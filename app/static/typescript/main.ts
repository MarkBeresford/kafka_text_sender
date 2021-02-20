import * as $ from 'jquery'

class KafkaTopic {
        topicId: string;
        divClass: string;
        secondDivClass: string;

        constructor(topicId: string, divClass: string, ) {
                this.topicId = topicId;
                this.divClass = divClass;
                this.secondDivClass = "message";
        }
}

export var firstTopic = new KafkaTopic('#Messages', 'mine messages');     
export var secondTopic = new KafkaTopic('#Messages', 'yours messages');

export async function getAllHistoricData(sender: number) {
        (await fetch("/getAllData"))
        .json()
        .then(dataArray => {
                dataArray['data']
                .forEach((element: string) => {
                        try{
                                let dataFromTopic = JSON.parse(element)
                                if(dataFromTopic['sender'] == sender) addKafkaDataToConversation(dataFromTopic['message'], firstTopic) 
                                else addKafkaDataToConversation(dataFromTopic['message'], secondTopic) 
                        } catch (err){
                                console.log(err)
                        }
                });
                
        })
}

export async function getDataFromTopic(endPoint: string, topic: KafkaTopic){ 
        (await fetch(endPoint)).json()
        .then((response: Response) => {
                return JSON.parse(response['data'])
        })
        .then((data: string) => {
                addKafkaDataToConversation(data['message'], topic)
        })
        getDataFromTopic(endPoint, topic)
    };

export function addKafkaDataToConversation(data: String, topic: KafkaTopic): void {
        var dataToAddToConversaton =
                ["<div class='", topic.divClass, "'><div class='", topic.secondDivClass, "'>", data, "</div>"]
                .join("")
        $(topic.topicId).append(dataToAddToConversaton)
}
