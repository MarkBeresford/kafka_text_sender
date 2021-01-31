import { getAllHistoricData, firstTopic, secondTopic, addKafkaDataToConversation, getDataFromTopic } from "./main"

window.onload = () => {
    getAllHistoricData(1)
    getDataFromTopic('/getTopicDataFromSender2', secondTopic)
}

const form: HTMLFormElement = document.querySelector('#firstUserForm');

form.onsubmit = () => {
    const formData = new FormData(form);
    const text = formData.get('textToSend') as string;
    console.log(text)
    addKafkaDataToConversation(text, firstTopic)
};
