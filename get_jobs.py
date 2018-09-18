import json
import requests
from jenkinsapi.jenkins import Jenkins
from datetime import datetime
import sqlite3
from sqlite3 import Error

"""Create the database"""
conn = sqlite3.connect('jobs.db')
c = conn.cursor()
c.execute("""CREATE TABLE if not exists jobs (
        name text,
        description text,
        running integer,
        enabled integer,
        checked_at text
    )""")


"""Get instence of Jenkins server"""
def get_server_instance():
    jenkins_url = 'http://jenkins_host:8080' # I don't know the exact url
    server = Jenkins(jenkins_url, username='foouser', password='foopassword')
    return server


"""Get job details of each job that is running on the Jenkins instance"""
def get_job_details():
    server = get_server_instance()
    for job_name, job_instance in server.get_jobs():
        print('Job Name:%s' % (job_instance.name))
        print ('Job Description:%s' % (job_instance.get_description()))
        print ('Is Job running:%s' % (job_instance.is_running()))
        print ('Is Job enabled:%s' % (job_instance.is_enabled()))

        c.execute("INSERT INTO jobs (?, ?, ?, ?, ?)", (
            job_instance.name, 
            job_instance.get_description(), 
            job_instance.is_running(), 
            job_instance.is_enabled(), 
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))

def main():
    get_job_details()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()