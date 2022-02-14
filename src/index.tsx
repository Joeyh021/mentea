import React, { useState } from "react";
import { FC } from "react";
import ReactDOM from "react-dom";



interface IFeedbackForm {
  id: string
}

interface IQuestion {
  id: string
  name: string
  desc?: string
  type: string // E.g. 'text' 'number' 'range' 'radio' etc
  type_data?: IQuestionTypeData
}

interface IQuestionTypeData {
  min?: number
  max?: number
  placeholder?: string
  options?: IQuestionOption[]

}

interface IQuestionOption {
  key: string
  value: string
}


const fakeQuestions: IQuestion[] = [
  {
    id: '7d331b08-9a2c-4f53-8356-77c85d349ca5',
    name: 'What is your name?',
    type: 'text',
    type_data: {
      placeholder: "John Doe"
    }
  },
  {
    id: 'a36e1ec0-a3f5-4103-8f46-51d75f42f495',
    name: "What colour's do you like?",
    type: 'checkbox',
    type_data: {
      options: [
        {
          key: "Red",
          value: "red-value-1"
        },
        {
          key: "Green",
          value: "Green-value-1"
        },
        {
          key: "Blue",
          value: "blue-value-1"
        }
      ]
    }
  },
  {
    id: '9be58d60-9b36-46b6-94b1-2eddab9fac1c',
    name: "Pick your fav group member!",
    type: 'radio',
    type_data: {
      options: [
        {
          key: "Noah",
          value: "noah"
        },
        {
          key: "Josh",
          value: "josh"
        },
        {
          key: "Joey",
          value: "joey"
        },
        {
          key: "Mia",
          value: "Mia"
        },
        {
          key: "Teo",
          value: "Teo"
        },
        {
          key: "Peter",
          value: "Peter"
        },
        {
          key: "Lukas",
          value: "Lukas"
        }
      ]
    }
  },
  {
    id: '52d1d0e1-d1b3-4f3d-b36a-568442c96cec',
    name: "Select a business area",
    type: 'select',
    type_data: {
      options: [
        {
          key: "Drug Smuggling",
          value: "ds"
        },
        {
          key: "Child Slavery",
          value: "cs"
        },
        {
          key: "Court Corruption",
          value: "cc"
        },
        {
          key: "Deformation of Bojo",
          value: "dob"
        },

      ]
    }
  }
]


const FeedbackFormViewer: FC<IFeedbackForm> = ({ id }) => {

  const [questions, setQuestions] = useState<IQuestion[]>(fakeQuestions)

  return (
    <div>
      <div>Form ID { id }</div>
      {
        questions.map(q => {
          return (
            <Question {...q} key={q.id} />
          )
        })
      }
    </div>
  )
}

const Question: FC<IQuestion> = ({ ...props }) => {

  if (props.type === "checkbox") {
    return (
      <CheckboxQuestion {...props} />
    )
  } else if (props.type === "radio") {
    return (
      <RadioQuestion {...props} />
    )
  } else if (props.type === "select" ){
    return (
      <SelectQuestion {...props} />
    )
  } else {

    return (
      <div className="mb-3">
        <label htmlFor={`form-question-${props.id}`} className="form-label">{ props.name }</label>

        <input type={props.type} placeholder={props.type_data?.placeholder} className="form-control" id={`form-question-${props.id}`} aria-describedby="emailHelp" />
        <div id={`form-question-${props.id}-help`} className="form-text">{ props.desc }</div>
      </div>
    )
  }

  return null
}

const CheckboxQuestion: FC<IQuestion> = ({ ...props }) => {
  return (
    <div className="mb-3">
        <label htmlFor={`form-question-${props.id}`} className="form-label">{ props.name }</label>


        <div>
          { props.type_data?.options?.map(option => {
            return (
              <div className="form-check form-check-inline">
                <input className="form-check-input" type="checkbox" id={`form-question-${props.id}-option-${option.key}`} value={option.value} />
                <label className="form-check-label" htmlFor={`form-question-${props.id}-option-${option.key}`}>{option.key}</label>
              </div>
            )
          })}
        </div>


        <div id={`form-question-${props.id}-help`} className="form-text">{ props.desc }</div>
      </div>
  )
}

const RadioQuestion: FC<IQuestion> = ({ ...props }) => {
  return (
    <div className="mb-3">
    <label htmlFor={`form-question-${props.id}`} className="form-label">{ props.name }</label>


    <div>
      { props.type_data?.options?.map(option => {
        return (
          <div className="form-check form-check-inline">
            <input className="form-check-input" type="radio" name={`form-question-${props.id}-radio`} id={`form-question-${props.id}-option-${option.key}`} value={option.value} />
            <label className="form-check-label" htmlFor={`form-question-${props.id}-option-${option.key}`}>{option.key}</label>
          </div>
        )
      })}
    </div>


    <div id={`form-question-${props.id}-help`} className="form-text">{ props.desc }</div>
  </div>
  )
}

const SelectQuestion: FC<IQuestion> = ({ ...props }) => {
  return (
    <div className="mb-3">
    <label htmlFor={`form-question-${props.id}`} className="form-label">{ props.name }</label>


    <select className="form-select" id={`form-question-${props.id}`} aria-label="Default select example">
      <option selected>Open this select menu</option>
      {
        props.type_data?.options?.map(option => {
          return (
            <option value={option.value}>{option.key}</option>
          )
        })
      }
    </select>


    <div id={`form-question-${props.id}-help`} className="form-text">{ props.desc }</div>
  </div>
  )
}







const Hi: FC = () => {
  return <div>Hello world</div>;
};










const forms: HTMLCollectionOf<Element> = document.getElementsByTagName('custom-form')


for (let i = 0; i < forms.length; i++) {
  let form = forms.item(i)
  ReactDOM.render(<FeedbackFormViewer id={form?.getAttribute('form-id') || 'no-id'} />, form);
}