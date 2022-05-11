from jira import JIRA
from collections import Counter
import lxml.etree as ET
import csv
import ftplib
import os

def get_active_openings():
    
    jira = JIRA(server="https://exceptionly.atlassian.net", basic_auth=("YOUR JIRA SUPERADMIN USER EMAIL HERE", "YOUR JIRA SUPERADMIN ACCESS TOKEN HERE"))

    issues = jira.search_issues('project=TEN AND issuetype="Opening" AND status="In Progress"', maxResults=100) 

    issue_dict = {'openings':{}}
    
    for issue in issues:
        issue_dict['openings'][issue.key] = {}
        issue_dict['openings'][issue.key]['fields'] = {}
        issue_dict['openings'][issue.key]['fields']['field'] = {}
        
        for key, value in issue.raw['fields'].items():

            issue_dict['openings'][issue.key]['fields']['field'][key] = value
    
    meta_dict={}

    source_dict = {'source':{}}
    source_dict['source'] = {}

    for key, value in issue_dict['openings'].items():
        issue_key = key
        meta_dict[issue_key] = {}
        meta_dict[issue_key]['salary'] = {}
        meta_dict[issue_key]['salary']['lowEnd'] = {'amount':'','currencyCode':''}
        meta_dict[issue_key]['salary']['highEnd'] = {'amount':'','currencyCode':''}
        meta_dict[issue_key]['salary']['period'] = {}
        meta_dict[issue_key]['salary']['type'] = {}

        for key, value in value['fields']['field'].items():
            if key=='customfield_10088' and value != None:
                meta_dict[issue_key].update({'company':'Exceptionly'})
                meta_dict[issue_key].update({'title':str(value)})
                
            elif key=='summary' and value != None:
                meta_dict[issue_key].update({'pipeline_name':str(value)})
            elif key=='customfield_10089' and value != None:
                meta_dict[issue_key].update({'description':str(value)})
                
            elif key=='customfield_10107' and value != None:
                
                skills_list=[]
                for item in value:
                    skills_list.append(item.replace('_',' '))

                skills_text = ', '.join(skills_list)
                meta_dict[issue_key].update({'skills':str(skills_text)})

            elif key=='customfield_10105' and value != None:
                meta_dict[issue_key].update({'benefits':str(value)})
                
            elif key=='customfield_10091' and value != None:
                meta_dict[issue_key].update({'applyUrl':str(value)})
                
            elif key=='customfield_10092' and value != None:
                meta_dict[issue_key].update({'partnerJobId':str(value)})
                
            elif key=='customfield_10094' and value != None:
                
                c_id = 0
                meta_dict[issue_key]['country'] = {}
                for item in value:
                    
                    meta_dict[issue_key]['country'].update({c_id:str(item['value'])})
                    c_id += 1
                c_id = 0
                
            elif key=='customfield_10102' and value != None:
                c_id = 0
                meta_dict[issue_key]['state'] = {}
                for item in value:
                    
                    meta_dict[issue_key]['state'].update({c_id:str(item['value'])})
                    c_id += 1
                c_id = 0
                
            elif key=='customfield_10095' and value != None:
                c_id = 0
                meta_dict[issue_key]['city'] = {}
                for item in value:
                    
                    meta_dict[issue_key]['city'].update({c_id:str(item['value'])})
                    c_id += 1
                c_id = 0
                
            elif key=='customfield_10090' and value != None:
                c_id = 0
                meta_dict[issue_key]['industry_code'] = {}
                for item in value:
                    
                    meta_dict[issue_key]['industry_code'].update({c_id:str(item['value'])})
                    c_id += 1
                c_id = 0
                
            elif key=='customfield_10097' and value != None:
                c_id = 0
                meta_dict[issue_key]['job_function'] = {}
                for item in value:
                    
                    meta_dict[issue_key]['job_function'].update({c_id:str(item['value'])})
                    c_id += 1
                c_id = 0
                
            elif key=='customfield_10101' and value != None:
                meta_dict[issue_key].update({'experienceLevel':str(value['value'])})
                
            elif key=='customfield_10104' and value != None:
                meta_dict[issue_key].update({'isRemote':str(value['value'])})
                
            elif key=='customfield_10098' and value != None:
                
                meta_dict[issue_key]['salary']['highEnd']['amount'] = str(int(value))
                

            elif key=='customfield_10099' and value != None:
                
                meta_dict[issue_key]['salary']['lowEnd']['amount'] = str(int(value))
                
            elif key=='customfield_10100' and value != None:

                meta_dict[issue_key]['salary']['lowEnd']['currencyCode'] = str(value['value'].split('-')[0])
                meta_dict[issue_key]['salary']['highEnd']['currencyCode'] = str(value['value'].split('-')[0])
                
            elif key=='customfield_10106' and value != None:
                meta_dict[issue_key]['salary']['period'] = str(value['value'])
                meta_dict[issue_key]['salary']['type'] = str('BASE_SALARY')
                
            elif key=='customfield_10096' and value != None:
                meta_dict[issue_key].update({'jobType':str(value['value'])})
                
            elif key=='customfield_10103' and value != None:
                meta_dict[issue_key].update({'workplaceTypes':str(value['value'])})
                
            else:
                pass
        
    validation =[] 
    
    for key, value in meta_dict.items():

        if 'city' not in value:
            validation.append(key)
            
    for key in validation:
        meta_dict.pop(key)

    validation = []
    
    job_slots_expected = 0
    job_slot_counter = 0
    
    for item in meta_dict:
        job_slots_expected += len(meta_dict[item]['city'])
        
        for key, value in meta_dict[item]['city'].items():
            
            source_dict['source'][str(item)+'-'+str(key)] = {}
            source_dict['source'][str(item)+'-'+str(key)]['issue_key'] = item
            source_dict['source'][str(item)+'-'+str(key)]['pipeline_name'] = meta_dict[item]['pipeline_name']
            source_dict['source'][str(item)+'-'+str(key)]['company'] = meta_dict[item]['company']
            source_dict['source'][str(item)+'-'+str(key)]['title'] = meta_dict[item]['title']
            source_dict['source'][str(item)+'-'+str(key)]['description'] = meta_dict[item]['description']
            source_dict['source'][str(item)+'-'+str(key)]['benefits'] = meta_dict[item]['benefits']
            source_dict['source'][str(item)+'-'+str(key)]['applyUrl'] = meta_dict[item]['applyUrl']
            source_dict['source'][str(item)+'-'+str(key)]['partnerJobId'] = meta_dict[item]['partnerJobId']+'_'+item+'_'+str(key)
            source_dict['source'][str(item)+'-'+str(key)]['salaries'] = {}
            source_dict['source'][str(item)+'-'+str(key)]['salaries'] = {'salary':{}}
            source_dict['source'][str(item)+'-'+str(key)]['salaries']['salary'] = {'lowEnd':{},'highEnd':{}, 'period':'', 'type':''}
            source_dict['source'][str(item)+'-'+str(key)]['salaries']['salary']['lowEnd']['amount'] = meta_dict[item]['salary']['lowEnd']['amount']
            source_dict['source'][str(item)+'-'+str(key)]['salaries']['salary']['highEnd']['amount'] = meta_dict[item]['salary']['highEnd']['amount']
            source_dict['source'][str(item)+'-'+str(key)]['salaries']['salary']['lowEnd']['currencyCode'] = meta_dict[item]['salary']['lowEnd']['currencyCode']
            source_dict['source'][str(item)+'-'+str(key)]['salaries']['salary']['highEnd']['currencyCode'] = meta_dict[item]['salary']['highEnd']['currencyCode']
            source_dict['source'][str(item)+'-'+str(key)]['salaries']['salary']['period'] = meta_dict[item]['salary']['period']
            source_dict['source'][str(item)+'-'+str(key)]['salaries']['salary']['type'] = meta_dict[item]['salary']['type']
            source_dict['source'][str(item)+'-'+str(key)]['experienceLevel'] = meta_dict[item]['experienceLevel']
            source_dict['source'][str(item)+'-'+str(key)]['skills'] = meta_dict[item]['skills']
            source_dict['source'][str(item)+'-'+str(key)]['isRemote'] = meta_dict[item]['isRemote']
            source_dict['source'][str(item)+'-'+str(key)]['jobType'] = meta_dict[item]['jobType']
            source_dict['source'][str(item)+'-'+str(key)]['workplaceTypes'] = meta_dict[item]['workplaceTypes']
            source_dict['source'][str(item)+'-'+str(key)]['jobFunctions'] = meta_dict[item]['job_function']
            source_dict['source'][str(item)+'-'+str(key)]['industryCodes'] = meta_dict[item]['industry_code']
            source_dict['source'][str(item)+'-'+str(key)]['city'] = value
            
    for item in source_dict['source'].items():
        job_slot_counter += 1
        
        meta_key = item[0].split('-')[0]+'-'+item[0].split('-')[1]

        for country in meta_dict[meta_key]['country'].items():

            city_country_code = item[1]['city'].split('-')[0]
            meta_country_code = country[1].split('-')[0]
            city = item[1]['city'].split('-')[1]
            country = country[1].split('-')[1]
            
            if city_country_code == meta_country_code and meta_country_code != 'US':
                item[1]['country'] = str(country)
                item[1]['location'] = '{}, {}'.format(city, country)
                
            elif city_country_code == meta_country_code and meta_country_code == 'US':
                for state in meta_dict[meta_key]['state'].items():

                    if US_city_state_checker(city, state[1]) and state[1]:
                        item[1]['country'] = str(country)
                        item[1]['state'] = str(state[1])
                        item[1]['location'] = '{}, {}'.format(city, get_state_shortcode(state[1]))
                        
                    else:
                        pass
            else:
                pass
    
        item[1]['city'] = item[1]['city'].split('-')[1]
        item[1]['applyUrl'] = str(item[1]['applyUrl']+'?source='+item[1]['partnerJobId']+'_'+item[1]['country']+'_'+item[1]['city'])
  
    if job_slot_counter != job_slots_expected:
        raise Exception('MISMATCH IN EXPECTATIONS: job_slot_counter: '+str(job_slot_counter)+' > job_slots_expected: '+str(job_slots_expected))
            
    print('\n\nTotal '+ str(job_slots_expected) + ' job slots expected\n\n')

    company_names = []

    root = ET.Element('source')
    
    for item in source_dict['source']:
        job = ET.SubElement(root, 'job')
        job.insert(0, ET.Comment('job_id: '+str(item)))
        for key, value in source_dict['source'][item].items():
            if key == 'job':
                ET.SubElement(job, key).text = ET.CDATA(value)
            elif key=='title':
                ET.SubElement(job, key).text = ET.CDATA(value)
            elif key=='applyUrl':
                ET.SubElement(job, key).text = ET.CDATA(value.replace(' ','_'))
            elif key=='partnerJobId':
                ET.SubElement(job, key).text = ET.CDATA(value)
            elif key == 'jobType':
                ET.SubElement(job, key).text = ET.CDATA(value)
            elif key == 'experienceLevel':
                ET.SubElement(job, key).text = ET.CDATA(value)
            elif key == 'skills':
                ET.SubElement(job, key).text = ET.CDATA(value)
            elif key == 'workplaceTypes':
                ET.SubElement(job, key).text = ET.CDATA(value)
            elif key == 'salaries':
                salaries = ET.SubElement(job, key)
                salary = ET.SubElement(salaries, 'salary')
                highEnd = ET.SubElement(salary, 'highEnd')
                ET.SubElement(highEnd, 'amount').text = ET.CDATA(source_dict['source'][item]['salaries']['salary']['highEnd']['amount'])
                ET.SubElement(highEnd, 'currencyCode').text = source_dict['source'][item]['salaries']['salary']['highEnd']['currencyCode']
                lowEnd = ET.SubElement(salary, 'lowEnd')
                ET.SubElement(lowEnd, 'amount').text = ET.CDATA(source_dict['source'][item]['salaries']['salary']['lowEnd']['amount'])
                ET.SubElement(lowEnd, 'currencyCode').text = source_dict['source'][item]['salaries']['salary']['lowEnd']['currencyCode']
                ET.SubElement(salary, 'period').text = ET.CDATA(source_dict['source'][item]['salaries']['salary']['period'])
                ET.SubElement(salary, 'type').text = ET.CDATA(source_dict['source'][item]['salaries']['salary']['type'])
            elif key == 'company':
                ET.SubElement(job, key).text = ET.CDATA(value)
            elif key == 'city':
                ET.SubElement(job, key).text = ET.CDATA(value)
            elif key == 'country':
                ET.SubElement(job, key).text = ET.CDATA(value)
            elif key == 'state':
                ET.SubElement(job, key).text = ET.CDATA(value)
            elif key == 'location':
                ET.SubElement(job, key).text = ET.CDATA(value)
            elif key =='isRemote':
                ET.SubElement(job, key).text = ET.CDATA(value)
            elif key == 'jobFunctions':
                jobFunctions = ET.SubElement(job, key)
                for func in value.items():
                    ET.SubElement(jobFunctions, 'jobFunction').text = ET.CDATA(func[1].split('-')[0])
            elif key == 'industryCodes':
                industryCodes = ET.SubElement(job, key)
                for func in value.items():
                    ET.SubElement(industryCodes, 'industryCode').text = ET.CDATA(func[1].split('-')[0])
            elif key == 'description':
                ET.SubElement(job, key).text = ET.CDATA(value+'\n#LI-SA1')
            elif key == 'benefits':
                ET.SubElement(job, key).text = ET.CDATA(value)
            elif key == 'pipeline_name':
                company_names.append(value.split('_')[0])
                
    file_path = os.path.abspath(os.path.dirname(__file__))
    file_name = os.path.join(file_path, 'exceptionlyjds.xml')

    ET.ElementTree(root).write(file_name, encoding='utf-8', xml_declaration=True)
    print('XML Creation: Done\n')


    if len(source_dict['source']) > 60:
        print(str(len(source_dict['source']))+'/60 job slots generated\nWARNING: More than 60 job slots were used. Please check the xml file')
    else:
        print(str(len(source_dict['source']))+'/60 job slots generated\nWARNING: Where are the other '+str(60-len(source_dict['source']))+' job slots?')

    company_counts = Counter(company_names)
    company_costs = {}
    for company in company_counts:
        company_costs[company] = company_counts[company] * 90

    company_list = []
    for company in company_costs:
        company_list.append({'Company Name': company, 'Total Count': company_counts[company], 'Total Cost': company_costs[company]})
        print('Company Name: '+company+'\nTotal Count: '+str(company_counts[company])+'\nTotal Cost: $'+str(company_costs[company])+'\n\n')

def US_city_state_checker(city=None, state=None):

    file_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(file_path, 'us-states.csv')
    
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if city in row and state in row:
                return True
    return False

def get_state_shortcode(state_long_name=None):

    file_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(file_path, 'us-states.csv')
    
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if state_long_name in row[1]:
                return row[0]
    return False

def file_upload(fname=None):

    host = '### YOUR HOST OR IP ADDRESS HERE ###'
    port = 21

    username = '####YOUR FTP USERNAME HERE####'
    password = '####YOUR FTP PASSWORD HERE ###'

    ftp = ftplib.FTP()
    ftp.connect(host, port)
    ftp.login(username, password)

    file_name = fname

    file_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(file_path, file_name)

    ftp.cwd('/public_html/')

    ftp.storbinary('STOR '+file_name, open(file_path, 'rb'))
    print('Successfully uploaded '+file_name+'\n')

if __name__ == "__main__":
    
    get_active_openings()
    file_upload('exceptionlyjds.xml')
    

    



