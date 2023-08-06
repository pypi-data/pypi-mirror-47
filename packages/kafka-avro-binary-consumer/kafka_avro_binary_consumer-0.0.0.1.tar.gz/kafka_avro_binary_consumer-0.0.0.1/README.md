First of all, we need to start confluent kafka server, use this article, to know how to do it:
    https://docs.confluent.io/3.0.0/control-center/docs/quickstart.html

The purpose of this project is:
	- consume binary avro, split it into different topics

To install this project, you need:
	- install all of packages, what are in packages folder
	- set up postgres server and execute create_config_tables.sql and insert_to_config_tables.sql files
	- put binary_avro_consumer.py and conf.cnf on server and execute python file with command
		python3.6 binary_avro_consumer.py (params)

More about console execution parameters:
	

Create tables statements are stored in create_config_tables.sql file.
Insert into config tables statements are stored in insert_to_config_tables.sql file.
You should execute the create statements, and insert into those tables your settings.
You got such structure for tables:


      config_key         |  config_value
     --------------------+----------------


      topic_name  | field_name
    --------------+-------------
    
End here is an example of their filling:

    --The config key, means the key of some setting, there an explanation of their meaning--
    
 ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
 
         bootstrap_server_from - The bootstrap server from what we have messages, can be multiple times in db, because of multiple bootstrap server, kafka is cluster.
         bootstrap_server_from_port - The port of those bootstrap servers, usually bootstrap servers have the same port.\
         schema_registry - The schema registry url, should starts with http:// or https://
         schema_registry_port - The schema registry port
         topic_read - The topic, from what we need to read messages, so this topic is from `bootstrap_server_from` server.
         group_id - Usually uses default name `example_avro`, this parameter required  for consuming
         bootstrap_server_to - The server to what we writes messages, what we read and modified in `bootstrap_server_from`
         bootstrap_server_to_port - The port of `bootstrap_server_to`
         from_beginning - start consuming from beginning 1 - true, 0 - false 
         count_messages_consume - count of messages, what consumes per one iteration

                 config_key         |  config_value
        ----------------------------+----------------
         bootstrap_server_from      | localhost
         bootstrap_server_from_port | 9092
         schema_registry            | http://0.0.0.0
         schema_registry_port       | 8081
         topic_read                 | avro-test
         group_id                   | example_avro
         bootstrap_server_to        | localhost
         bootstrap_server_to_port   | 9092
         from_beginning             | 1
         count_messages_consume     | 100

         
 ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------   


     topic_name  | field_name
    --------------+-------------
     first_topic  | uid
     first_topic  | somefield
     second_topic | options hel
     second_topic | options mel
     
     
    For example, you have such avro schema:
    
      "namespace" : "my.com.ns",
      "name": "myrecord",
      "type" :  "record",
      "fields" : [
         {"name": "uid", "type": "int"},
         {"name": "somefield", "type": "string"},
         {"name": "options", "type": {
            "type": "array",
            "items": {
                "type": "record",
                "name": "lvl2_record",
                "fields": [
                    {"name": "hel", "type": "string"},
                    {"name": "mel", "type": "string"}
                     }
                   ]
                }
            }
         }
         
      ]
    }

    You need to extract such values from this schema: 
    
    uid, somefield, options->hel, options->mel, and you need to store this values in first_topic and second_topic, so for example, we store uid and somefield in first_topic, 
        and options->hel, options->mel in second_topic. options->hel, options->mel means that field hel is a child of options, the same for mel.
        
    So we write to db: first_topic uid,somefield  , what means, plz store uid and somefield in first_topic, the same for second_topic.
    
 ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------        


How to understand where actually your avro schema stored in schema registry?
Here you an answer:

Imagine, that you created a topic named test, and registered a schema to schema registry, to know what schema is, and to track if that schema changed, you need:
    To execute such command in terminal, schema registry server should work (insted of http://localhost:8081/subjects you should put you schema registry url):
	curl -X GET http://localhost:8081/subjects
    
	Output of curl: ["Kafka-value","Kafka-key","test-value"]
    
    You see, that your test topic also created 'test-value' subject, so the schema what you need is
    http://localhost:8081/subjects/test-value/versions/latest",
    in some cases your schema can be situated by `Kafka-value` path, so your url will be:  http://localhost:8081/subjects/Kafka-value/versions/latest"
    
	Change this url conf.cnf file, more about conf.cnf:

    conf.cnf, is config for python script:

        On FIRST line is schema registry url.
        On SECOND line is DB name.
        On THIRD line is username.
        On fourth line is password.
        On sixth line is host.
	On the seventh line is the number of avro messages to produce by AvroProducer.
	
    
    
After all of this, you need to start the script called pushpop_complex_avro.py, 
by such command python3.6 pushpop_complex_avro.py (optional params -d -i -e, for debug,info,error respectively).
After script is running, it wait for messages, so you need to produce messages to topic_read:
    python3.6 avro_producer.py
And see, that messages were splited and directed to first_topic and second_topic.

