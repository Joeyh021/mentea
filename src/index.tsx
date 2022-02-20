import axios from "axios";
import React, { useEffect, useState } from "react";
import { FC } from "react";
import ReactDOM from "react-dom";
import FormBuilder from "./form-builder";



interface IFeedbackFormProps {
  id: string
}

interface IFeedbackForm {
  id: string
  name: string
  desc: string
}

export interface IQuestion {
  id: string
  name: string
  desc?: string
  type: string // E.g. 'text' 'number' 'range' 'radio' etc
  type_data?: IQuestionTypeData
  required: boolean
}

export interface IQuestionTypeData {
  min?: number
  max?: number
  step?: number
  placeholder?: string
  options?: IQuestionOption[]

}

export interface IQuestionOption {
  key: string
  value: string
}


export const fakeQuestions: IQuestion[] = [
  {
    id: '7d331b08-9a2c-4f53-8356-77c85d349ca5',
    name: 'What is your name?',
    type: 'text',
    type_data: {
      placeholder: "John Doe"
    },
    required: true
  },
  {
    id: '7d331b08-9a2c-5f53-8356-77c85d349ca5',
    name: 'Pick a number',
    type: 'number',
    type_data: {
      placeholder: "0"
    },
    required: false
  },
  {
    id: '7d331b08-9a2c-4f53-8356-77c85d349ca5',
    name: 'What is your email?',
    type: 'email',
    type_data: {
      placeholder: "bee@movie.com"
    },
    required: true
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
    },
    required: true
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
    },
    required: true
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
    },
    required: true
  },
  {
    id: '1a331b08-9a2c-4f53-8356-77c85d349ca5',
    name: 'Write a short story',
    type: 'textarea',
    required: true
  },
]


const FeedbackFormViewer: FC<IFeedbackFormProps> = ({ id }) => {

  const [error, setError] = useState<string | null>(null)

  const [questions, setQuestions] = useState<IQuestion[]>([])

  const [formData, setFormData] = useState<IFeedbackForm>({id: 'Loading...', name: 'Loading Form Name...', desc: ""})

  useEffect(() => {
    loadFormFromId(id)
  }, [id])

  const loadFormFromId = (formId :string) => {

    

    axios.get(`/feedback-api/${formId}/`).then(res => {
      setFormData(res.data.formData)
      setQuestions(res.data.questions)
    }).catch(e => {
      setError("No form was found with the given ID, or it could not be loaded!")
    })

    
  }


  return (
    <>
    {
      error === null && 
      <form>
      <h1>{ formData.name || 'Give me a name!' }</h1>
      <p>{ formData.desc || "Give me a description above! (If you leave it blank then I won't show up when actually used!)" }</p>
      {
        questions.map(q => {
          return (
            <div key={q.id} className="pb-1">
              <Question {...q} key={q.id} />
            </div>
          )
        })
      }

      <button type="submit" className="btn btn-primary">Submit</button>
    </form>
    } 
    {
      error &&
      <div className="alert alert-danger">
        { error }
      </div>
    }
    </>
  )
}


export const Question: FC<IQuestion> = ({ ...props }) => {

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
  } else if (props.type === "textarea" ){
    return (
      <TextareaQuestion {...props} />
    )
  } else if (props.type === "range" ){
    return (
      <RangeQuestion {...props} />
    )
  } else {

    return (
      <div className="mb-3">
        <div className="d-flex justify-content-between align-items-end">
          <label htmlFor={`form-question-${props.id}`} className="form-label">{ props.name }</label>

          { props.required && <p className="text-end mt-0 mb-0 text-danger" style={{'fontSize': '.8rem'}}>Required *</p>}
        </div>
        
        <input type={props.type} placeholder={props.type_data?.placeholder} className="form-control" id={`form-question-${props.id}`} onKeyPress={e => e.key === 'Enter' && e.preventDefault()} aria-describedby="emailHelp" required={props.required} />
        <div id={`form-question-${props.id}-help`} className="form-text">{ props.desc }</div>
      </div>
    )
  }

  return null
}

export const CheckboxQuestion: FC<IQuestion> = ({ ...props }) => {
  return (
    <div className="mb-3">
          <div className="d-flex justify-content-between align-items-end">
          <label htmlFor={`form-question-${props.id}`} className="form-label">{ props.name }</label>

          { props.required && <p className="text-end mt-0 mb-0 text-danger" style={{'fontSize': '.8rem'}}>Required *</p>}
        </div>
        <div>
          { props.type_data?.options?.map(option => {
            return (
              <div key={option.value} className="form-check form-check-inline">
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

export const RadioQuestion: FC<IQuestion> = ({ ...props }) => {
  return (
    <div className="mb-3">
  <div className="d-flex justify-content-between align-items-end">
          <label htmlFor={`form-question-${props.id}`} className="form-label">{ props.name }</label>

          { props.required && <p className="text-end mt-0 mb-0 text-danger" style={{'fontSize': '.8rem'}}>Required *</p>}
        </div>
    <div>
      { props.type_data?.options?.map(option => {
        return (
          <div key={option.value} className="form-check form-check-inline">
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

export const SelectQuestion: FC<IQuestion> = ({ ...props }) => {
  return (
    <div className="mb-3">
  <div className="d-flex justify-content-between align-items-end">
          <label htmlFor={`form-question-${props.id}`} className="form-label">{ props.name }</label>

          { props.required && <p className="text-end mt-0 mb-0 text-danger" style={{'fontSize': '.8rem'}}>Required *</p>}
        </div>
    <select className="form-select" id={`form-question-${props.id}`} aria-label="Default select example" required={props.required}>
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

export const TextareaQuestion: FC<IQuestion> = ({ ...props }) => {
  return (
    <div className="mb-3">
  <div className="d-flex justify-content-between align-items-end">
          <label htmlFor={`form-question-${props.id}`} className="form-label">{ props.name }</label>

          { props.required && <p className="text-end mt-0 mb-0 text-danger" style={{'fontSize': '.8rem'}}>Required *</p>}
        </div>
    <textarea id={`form-question-${props.id}`} rows={3} className="form-control"></textarea>


    <div id={`form-question-${props.id}-help`} className="form-text">{ props.desc }</div>
  </div>
  )
}

export const RangeQuestion: FC<IQuestion> = ({ ...props }) => {


  const calcSteps = () => {

    if ((props.type_data?.step || 0) < 0) return

    let steps: number = (((props.type_data?.max || 100) + 1 - (props.type_data?.min || 0))) / (props.type_data?.step || 10);
    return Math.round(steps);
  }

  return (
    <div className="mb-3">
      <div className="d-flex justify-content-between align-items-end">
        <label htmlFor={`form-question-${props.id}`} className="form-label">{ props.name }</label>

        { props.required && <p className="text-end mt-0 mb-0 text-danger" style={{'fontSize': '.8rem'}}>Required *</p>}
      </div>

      
      <input type={props.type} placeholder={props.type_data?.placeholder} min={props.type_data?.min} max={props.type_data?.max} step={props.type_data?.step} className="form-range" style={{padding: '0'}} id={`form-question-${props.id}`}  aria-describedby="emailHelp" required={props.required} />
      
      <div className="d-flex justify-content-between position-relative " style={{marginLeft: "7px", marginRight: "7px"}}>
        <div className="position-relative">
          <div style={{height: "10px", width: "1px", backgroundColor: 'black'}} />
          <div className="position-absolute top-100 " style={{width: "10px", height: "10px", left: "-3.5px"}}>
            { props.type_data?.min }
          </div>
        </div>
        <div className="position-relative">
          <div style={{height: "10px", width: "1px", backgroundColor: 'black'}} />
          <div className="position-absolute top-100 " style={{width: "10px", height: "10px", left: "-3.5px"}}>
            { props.type_data?.max }
          </div>
        </div>
        
      </div>
      
      <div id={`form-question-${props.id}-help`} className="form-text">{ props.desc }</div>
    </div>
  )
}




const Hi: FC = () => {
  return <div>Hello world</div>;
};










const forms: HTMLCollectionOf<Element> = document.getElementsByTagName('custom-form')

const formBuilders: HTMLCollectionOf<Element> = document.getElementsByTagName('custom-form-builder')


for (let i = 0; i < forms.length; i++) {
  let form = forms.item(i)
  ReactDOM.render(<FeedbackFormViewer id={form?.getAttribute('form-id') || 'no-id'} />, form);
}

for (let i = 0; i < formBuilders.length; i++) {
  let form = formBuilders.item(i)
  ReactDOM.render(<FormBuilder />, form);
}