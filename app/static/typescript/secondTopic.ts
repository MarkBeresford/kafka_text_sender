import { getAllHistoricData, firstTopic, secondTopic, addKafkaDataToConversation, getDataFromTopic } from "./main"

window.onload = () => {
    getAllHistoricData(2)
    getDataFromTopic('/getTopicData/1', secondTopic)
}

const form: HTMLFormElement = document.querySelector('#secondUserForm');

form.onsubmit = () => {
    const formData = new FormData(form);
    const text = formData.get('textToSend') as string;
    console.log(text)
    addKafkaDataToConversation(text, firstTopic)
};