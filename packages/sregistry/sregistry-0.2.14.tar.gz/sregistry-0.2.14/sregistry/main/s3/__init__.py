'''

Copyright (C) 2018-2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

'''

from sregistry.auth import read_client_secrets
from sregistry.logger import ( RobotNamer, bot )
from sregistry.main import ApiConnection
import boto3
import json
import os

from .query import ( 
    search, 
    search_all, 
    container_search 
)
from .pull import pull
from .push import push
from .delete import delete

class Client(ApiConnection):

    def __init__(self, secrets=None, base=None, **kwargs):
 
        self.base = base
        self._update_secrets()
        self._update_headers()
        super(ApiConnection, self).__init__(**kwargs)

    def _speak(self):
        '''add the bucket'''
        bot.info('[bucket:s3://%s]' % self.bucket)

    def __str__(self):
        return type(self)

    def _read_response(self,response, field="detail"):
        '''attempt to read the detail provided by the response. If none, 
        default to using the reason'''

        try:
            message = json.loads(response._content.decode('utf-8'))[field]
        except:
            message = response.reason
        return message


    def get_bucket_name(self):
        '''get or return the s3 bucket name. If not yet defined via an environment
           variable or setting, we create a name with the pattern.
                    sregistry-<robotnamer>-<1234>

           You can use the following environment variables to determine
           interaction with the bucket:
           
           SREGISTRY_S3_BUCKET: the bucket name (all lowercase, no underscore)
           
        '''
        # Get bucket name
        bucket_name = 'sregistry-%s' % RobotNamer().generate()
        self.bucket_name = self._get_and_update_setting('SREGISTRY_S3_BUCKET', 
                                                        bucket_name)


    def get_bucket(self):
        '''given a bucket name and a client that is initialized, get or
           create the bucket.
        '''
        for attr in ['bucket_name', 's3']:
            if not hasattr(self, attr):
                bot.exit('client is missing attribute %s' %(attr))

        self.bucket = self.s3.Bucket(self.bucket_name)
        # See if the bucket is already existing by checking the creation_date
        if self.bucket.creation_date is None:
            self.bucket = None
 
        # If the bucket doesn't exist, create it
        if self.bucket is None:
            self.bucket = self.s3.create_bucket(Bucket=self.bucket_name)
            bot.info('Created bucket %s' % self.bucket.name )

        return self.bucket


    def get_resource(self):
        '''use the user provided endpoint and keys (from environment) to
           connect to the resource. We can share the aws environment
           variables:

           AWS_ACCESS_KEY_ID
           AWS_SECRET_ACCESS_KEY

           https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html
        '''

        # s3.ServiceResource()
        self.s3 = boto3.resource('s3',
                                 endpoint_url=self.base,
                                 aws_access_key_id=self._id,
                                 aws_secret_access_key=self._key,
                                 config=boto3.session.Config(signature_version=self._signature))


    def _update_secrets(self, base=None):
        '''update secrets will update/get the base for the server, along
           with the bucket name, defaulting to sregistry.
        '''
        # We are required to have a base, either from environment or terminal
        self.base = self._get_and_update_setting('SREGISTRY_S3_BASE', self.base)
        self._id = self._required_get_and_update('AWS_ACCESS_KEY_ID')
        self._key = self._required_get_and_update('AWS_SECRET_ACCESS_KEY')

        # Get the desired S3 signature.  Default is the current "s3v4" signature.
        # If specified, user can request "s3" (v2 old) signature
        self._signature = self._get_and_update_setting('SREGISTRY_S3_SIGNATURE')

        if self._signature == 's3':
            # Requested signature is S3 V2
            self._signature = 's3'
        else:
            # self._signature is not set or not set to s3 (v2), default to s3v4
            self._signature = 's3v4'

        # Define self.bucket_name, self.s3, then self.bucket
        self.get_bucket_name()
        self.get_resource()
        self.get_bucket()


Client.pull = pull
Client.push = push
Client.search = search
Client.delete = delete
Client._search_all = search_all
Client._container_search = container_search
