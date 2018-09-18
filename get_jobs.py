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
def get_server_instance(username, password):
    jenkins_url = 'http://jenkins_host:8080' # I don't know the exact url
    server = Jenkins(jenkins_url, username='foouser', password='foopassword')
    return server


"""Get job details of each job that is running on the Jenkins instance"""
def get_job_details(username, password):
    server = get_server_instance(username, password)
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
    username = input('Your Jenkins account username: ')
    password = input('Your Jenkins account password: ')
    if username and password:
        try:
            print('Fetching your Jenkins jobs....')
            get_job_details(username, password)
        except Exception:
            print("Invalid username or password. Please Check your credentails and try again.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()