from flask import jsonify
import requests
import json
import jenkinsapi
from jenkinsapi.jenkins import Jenkins

class JenkinsWebBased:
    def __init__(self,user,password,url) -> None:
        self.Jenkins_url = url
        self.jenkins_user = user
        self.jenkins_pwd = password
    def JobList(self):
        try:
            auth= (self.jenkins_user, self.jenkins_pwd)
            jobs= requests.get(f"http://{self.Jenkins_url}/api/json?tree=jobs[name,color,displayName,description,url,builds[result,building,number,duration,estimatedDuration]],pretty=true",auth=auth)
            return jobs.json()
        except Exception as e:
            return {"Erreur":str(e)}
    def Summary(self):
        try:
            auth= (self.jenkins_user, self.jenkins_pwd)
            print(f"http://{self.Jenkins_url}/api/json?tree=jobs[name,color,displayName,description,url,builds[result,building,number,duration,estimatedDuration]],pretty=true")
            jobs= requests.get(f"http://{self.Jenkins_url}/api/json?tree=jobs[name,color,displayName,description,url,builds[result,building,number,duration,estimatedDuration]],pretty=true",auth=auth)
            all= jobs.json()
            jobscount=len(all["jobs"])
            buildcounts=0
            failure=0
            for j in all["jobs"]:
                buildcounts+=len(j["builds"])
                for b in j["builds"]:
                    if not b["result"]=='SUCCESS':
                        failure+=1
            integrations=jobscount
            return jobscount,buildcounts,failure,integrations

        except Exception as e:
            return {"Erreur--":str(e)}



