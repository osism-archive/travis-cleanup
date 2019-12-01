# travis-cleanup

We use Travis CI for testing our public repositories. The jobs create instances, keypairs, ..
on our OpenStack environment. Sometimes artifacts remain after the completion of a job, e.g.
because it was terminated unexpectedly. These artifacts occupy resources unnecessarily and
are regularly deleted by this script.

Workflow
--------

![Workflow](https://raw.githubusercontent.com/osism/travis-cleanup/master/images/workflow.png)

1. Get all existing security groups, keypairs, instances, and floating ip addresses
2. Extract the Travis CI job id from the names of the resources and get the status of th
   jobs from Travis CI
3. If the job has already been completed, delete the corresponding resource

Usage
-----

* Create `configuration/clouds.yml` on basis of `configuration/clouds.yml.sample`
* Create `configuration/secure.yml` on basis of `configuration/secure.yml.sample`
* Build the container image with `docker-compose build`
* Start the container with `docker-compose up -d`

License
-------

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Author information
------------------

This script was created by [Betacloud Solutions GmbH](https://betacloud-solutions.de).
