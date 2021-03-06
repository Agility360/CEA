#=============================================================
# written by: lawrence mcdaniel
# date: 31-july-2017
#
# purpose:  connection handler for Candidate Engagement App (CEA)
#           REST api. this function does the following:
#           1. connects to MySQL,
#           2. parses input parameters from the http request body,
#           3. formats and SQL string of the stored procedure call,
#           4. executes the stored procedure
#           5. return response object.
#=============================================================
import sys
import logging
import rds_config
import pymysql
import json


#rds_config is just a json string of the RDS MySQL connection parameters
#stored in a text file with a .py extension
#
#it is included in the build package that i uploaded to created this function
#it is not viewable from the AWS Lambda console
#==============================================================
rds_host  = rds_config.db_endpoint
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def lambda_handler(event, context):
    logger.info('JSON received is:' + str(event))

    retval = {}

    #
    # 1. connect to the MySQL database
    #
    try:
        conn = pymysql.connect(rds_host, user=name,
                               passwd=password, db=db_name, connect_timeout=2)
    except Exception as e:
        logger.error("ERROR: Could not connect to MySql instance.")
        logger.error(e)
        #sys.exit()
        retval["response"] = "failure"
        retval["err"] = str(e)
        return retval

    logger.info("Connected to RDS mysql instance.")



    #
    # 2. parse the input parameters from the https request body
    #    which is passed to this Lambda function from a AWS API Gateway method object
    #


    #
    # 3. create the SQL string
    #
    sql = "CALL sp_candidate_edit('%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, %d, '%s', '%s')" % (event['account_name'], event['first_name'],
                                            event['middle_name'], event['last_name'], event['email'], event['phone_number'],
                                            event['industry_id'], event['subindustry_id'], event['profession_id'], event['subprofession_id'],
                                            event['job_hunting'], event['city'], event['state'])

    #
    # 4. execute the SQL string
    #

    try:
        logger.info("Executing SQL statement: " + sql)
        cursor =  conn.cursor()
        cursor.execute(sql)
        cursor.close ()
        conn.close ()
    except Exception as e:
        logger.error("ERROR: MySQL returned an error.")
        logger.error(e)
        retval["response"] = "failure"
        retval["err"] = str(e)
        return retval


    #
    # 5. Generate return object
    #
    retval["response"] = "success"
    return retval
