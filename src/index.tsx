import React from "react";
import { FC } from "react";
import ReactDOM from "react-dom";



interface IFeedbackForm {
  id: string
}

interface IQuestion {
  type: string // E.g. 'text' 'number' 'range' 'radio' etc
  type_data: IQuestionTypeData
}

interface IQuestionTypeData {
  min?: number
  max?: number
  options:

}

interface IQuestionOption {
  key: string
  value: string
}





const FeedbackFormViewer: FC<IFeedbackForm> = ({ id }) => {
  return (
    <div>Form ID { id }</div>
  )
}







const Hi: FC = () => {
  return <div>Hello world</div>;
};











const domContainer = document.querySelector("#test");
ReactDOM.render(<FeedbackFormViewer id={domContainer?.getAttribute('form-id') || 'no-id'} />, domContainer);
