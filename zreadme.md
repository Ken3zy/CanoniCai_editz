Jsserv makemigrations base
Jsserv migrate
Jsserv runserver 0.0.0.0:8000

login http://0.0.0.0:8000/

actions load local local_app/twilio_bot.py
actions load local local_app/flow.py
actions load local local_app/cre_dataset.py


actions load module jaseci_ai_kit.use_qa
actions load module jaseci_ai_kit.use_enc
actions load module jaseci_ai_kit.bi_enc
actions load module jaseci_ai_kit.ent_ext
actions load module jaseci_ai_kit.cl_summer


graph delete active:graph
jac build _main.jac
graph create -set_active true
sentinel register -set_active true -mode ir _main.jir


walker run init

jac build _main.jac
sentinel set -snt active:sentinel -mode ir _main.jir
walker run init

graph get -mode dot -o .main.dot 
dot -Tpng .main.dot -o .main.png


## ent_ext
jac run .ent_ext.jac -walk train_and_val_flair -ctx "{\"train_file\":\"local_app/data/que_dataset.json\",\"val_file\":\"local_app/data/que_dataset.json\",\"test_file\":\"local_app/data/que_dataset.json\",\"model_name\":\"prajjwal1/bert-tiny\",\"model_type\":\"trfmodel\",\"num_train_epochs\":\"10\",\"batch_size\":\"8\",\"learning_rate\":\"0.02\"}"
jac run .ent_ext.jac -walk predict_flair -ctx "{\"text\":\"I would like to create an appointment. my son needs a manbun on saturday at 4 pm. \"}"

-- serv
walker run train_and_val_flair -ctx "{\"train_file\":\"local_app/data/que_dataset.json\",\"val_file\":\"local_app/data/que_dataset.json\",\"test_file\":\"local_app/data/que_dataset.json\",\"model_name\":\"prajjwal1/bert-tiny\",\"model_type\":\"trfmodel\",\"num_train_epochs\":\"20\",\"batch_size\":\"8\",\"learning_rate\":\"0.02\"}"
walker run predict_flair -ctx "{\"text\":\"I would like to create an appointment. my son needs a manbun on saturday at 4 pm. \"}"


## bi_enc
jac run .bi_enc.jac -walk bi_encoder_train -ctx "{\"train_file\": \"local_app/data/_clf_dataset.json\"}"
jac run .bi_enc.jac -walk bi_encoder_infer -ctx "{\"labels\": [\"appointment\", \"i have a question\", \"cost of service\",\"yes\",\"no\"]}"
jac run .bi_enc.jac -walk bi_encoder_save_model -ctx "{\"model_path\": \"dialogue_intent_model\"}"
jac run .bi_enc.jac -walk bi_encoder_load_model -ctx "{\"model_path\": \"dialogue_intent_model\"}"

--serv
walker run bi_encoder_train -ctx "{\"train_file\": \"local_app/data/_clf_dataset.json\"}"
walker run bi_encoder_infer -ctx "{\"labels\": [\"appointment\", \"i have a question\", \"cost of service\",\"yes\",\"no\"]}"
walker run bi_encoder_save_model -ctx "{\"model_path\": \"dialogue_intent_model\"}"
walker run bi_encoder_load_model -ctx "{\"model_path\": \"dialogue_intent_model\"}"


walker run talker -ctx "{\"question\": \"how much for a mohawk\"}"
walker run talker -ctx "{\"question\": \"what time do you open\"}"
walker run talker -ctx "{\"question\": \"yes\"}"
walker run talker -ctx "{\"question\": \"hi\"}"
walker run talker -ctx "{\"question\": \"my son also want a haircut. I think he want a buzzcut on sunday at 5 pm. Can you set that up too\"}"


walker run createGraph -ctx "{\"intent\": [\"greetings\", \"goodbye\", \"faq_question\"]}"
walker run createGraph -ctx "{\"intent\": [\"greetings\", \"goodbye\", \"cost\",\"faq_question\",\"cancel\",\"appointment\"]}"
walker run createGraph -ctx "{\"intent\": [\"greetings\", \"goodbye\", \"cost\"]}"
walker run createGraph -ctx "{\"intent\": [\"greetings\", \"goodbye\", \"appointment\", \"cost\"]}"


ec8bfaa76f71362dbe76fb41713fbdc818b94f4f7e19d3109641bed0192a7d13

urn:uuid:ea864a26-4ab2-4237-8e8a-b995dece9c04

urn:uuid:a9af431e-e528-4074-885f-000565c7b7e9
// callback
/*

                        Register Sentinel
curl --request POST \
  --url http://localhost:8000/js/sentinel_register \
  --header 'Authorization: token ec8bfaa76f71362dbe76fb41713fbdc818b94f4f7e19d3109641bed0192a7d13' \
  --header 'Content-Type: application/json' \
  --data '{ "name": "sentinel1", "code": "walker sample_walker: anyone {\r\n\thas fieldOne;\r\n\twith entry {\r\n\t\treport 1;\r\n\t}\r\n}" }'

[{"version":null,"name":"sentinel1","kind":"generic","jid":"urn:uuid:73c80d34-6a87-44ce-a5f4-cc811668c8da","j_timestamp":"2022-11-02T13:54:26.209724","j_type":"sentinel","code_sig":"4316e699b5980320f433e43e100a060c"},{"name":"root","kind":"node","jid":"urn:uuid:2a81a9f5-2317-4a30-bcb3-248ac8daa074","j_timestamp":"2022-11-02T13:54:26.210054","j_type":"graph","context":{}}]%     


                        Spawn Public Walker
curl --request POST \
  --url http://localhost:8000/js/walker_spawn_create \
  --header 'Authorization: token ec8bfaa76f71362dbe76fb41713fbdc818b94f4f7e19d3109641bed0192a7d13' \
  --header 'Content-Type: application/json' \
  --data '{ "name": "sample_walker", "snt":"active:sentinel" }'

{"name":"sample_walker","kind":"walker","jid":"urn:uuid:d59871e4-5fe2-4d28-9af4-c4088e7337ca","j_timestamp":"2022-11-02T13:57:50.653829","j_type":"walker","context":{}}%                                                                                                     


                        Getting Public Key
curl --request POST \
  --url http://localhost:8000/js/walker_get \
  --header 'Authorization: token ec8bfaa76f71362dbe76fb41713fbdc818b94f4f7e19d3109641bed0192a7d13' \
  --header 'Content-Type: application/json' \
  --data '{ "mode": "keys", "wlk": "spawned:walker:sample_walker", "detailed": false }'

{"anyone":"a30b1b9e374e02b4730574fccd04041e"}%                                                                                         


// http://0.0.0.0:8000/js_public/walker_callback/nodeID/walkerID?key=publicKey
// http://0.0.0.0:8000/js_public/walker_callback/fdd6b9e7-cfd9-4770-a610-94ee1e0cb866/73c80d34-6a87-44ce-a5f4-cc811668c8da?key=a30b1b9e374e02b4730574fccd04041e