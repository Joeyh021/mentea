import axios from "axios";
import React, { useEffect, useState } from "react";
import { FC } from "react";
import ReactDOM from "react-dom";
import { FieldValues, useForm, UseFormRegister } from "react-hook-form";
import FormBuilder from "./form-builder";
import ResultViewer from "./result-viewer";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";


export interface IFeedbackFormProps {
  id: string
}

export interface IFeedbackForm {
  id: string
  name: string
  desc: string
  acceptingSubmissionsUntil: string | null
  allowsMultipleSubmissions: boolean
  allowsEditingSubmissions: boolean
  
}

export interface IQuestion {
  id: string
  name: string
  desc?: string
  type: string // E.g. 'text' 'number' 'range' 'radio' etc
  type_data?: IQuestionTypeData
  required: boolean
  readonly?: boolean
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

interface IAnswerableQuestion extends IQuestion {
  register: UseFormRegister<FieldValues> | undefined
  errors: {[error: string]: any} | undefined

}

export interface ISubmission {
  formId: string
  answers: IAnswer[]
}

export interface IStoredSubmission {
  id: string
}

export interface IAnswer {
  q: string
  a: any
}

export enum EFormState {
  SUBMITTED, LOADING, READY
}


const FeedbackFormViewer: FC<IFeedbackFormProps> = ({ id }) => {

  const [error, setError] = useState<string | null>(null)



  const [loading, setLoading] = useState<boolean>(false)

  const [questions, setQuestions] = useState<IAnswerableQuestion[]>([])

  const [formData, setFormData] = useState<IFeedbackForm>({id: 'Loading...', name: 'Loading Form Name...', desc: "", allowsEditingSubmissions: false, allowsMultipleSubmissions: true, acceptingSubmissionsUntil: null})

  const { register, handleSubmit, formState: { errors }, reset, setValue } = useForm()

  const [state, setState] = useState<EFormState>(EFormState.LOADING)

  const [recentSubmission, setRecentSubmission] = useState<IStoredSubmission>()

  const [prevSubmissions, setPreviousSubmissions] = useState<IStoredSubmission[]>([])

  const [isEditing, setEditing] = useState<boolean>(false)

  const [readOnly, setReadOnly] = useState<boolean>(false)

  useEffect(() => {
    loadFormFromId(id)
  }, [id])

  // Immediately load previous answers if the form can only be submitted once and they already have a submission!
  useEffect(() => {
    if (!formData.allowsMultipleSubmissions && prevSubmissions.length !== 0) {
      let subId: string = prevSubmissions[0].id
      // Load submission here

      axios.get(`/feedback-api/submission/${subId}`).then(res => {
        let ans: IAnswer[] = []

        let data: [] = res.data.answers
        data.forEach((d: {associated_question: string, data: any}) => {
          ans.push({a: d.data, q: d.associated_question})
        })

        ans.forEach(a => setValue(a.q, a.a))
      })

      setEditing(true)
    }
  }, [formData.allowsMultipleSubmissions, prevSubmissions])

  useEffect(() => {

    setReadOnly(!formData.allowsMultipleSubmissions && !formData.allowsEditingSubmissions && prevSubmissions.length > 0)
  }, [formData, prevSubmissions])

  const loadFormFromId = (formId :string) => {

    

    axios.get(`/feedback-api/${formId}/`).then(res => {
      setFormData({...res.data.formData, id: formId})
      setQuestions(res.data.questions)
      setPreviousSubmissions(res.data.previousSubmissions || [])
      setState(EFormState.READY)
    }).catch(e => {
      setError("No form was found with the given ID, or it could not be loaded!")
    })

    
  }

  const submitForm = (data: any) => {

    setLoading(true)
    let answers: IAnswer[] = []

    Object.entries(data).forEach((entry: any) => {
      answers.push({
        q: entry[0],
        a: entry[1]
      })
    })

    let submission: ISubmission = {
      formId: formData.id,
      answers: answers
    }

    console.log(submission)

    let fd = new FormData()
    fd.append('jsonData', JSON.stringify(submission))

    let submitUrl = '/feedback-api/submission/'

    if (isEditing) {
      submitUrl = '/feedback-api/submission-update/'
      let ss: {submissionId: string, answers: IAnswer[]} = {submissionId: prevSubmissions[0].id, answers: answers}
      fd.set('jsonData', JSON.stringify(ss))
    }


  

    axios.post(submitUrl, fd).then(res => {
      if (res.data.result === "success") {
        setState(EFormState.SUBMITTED)

        let ss: IStoredSubmission = { id: res.data.data}

        setFormData(formData)
        setPreviousSubmissions([...prevSubmissions || [], ss])
         setRecentSubmission(ss)
      }

    }).finally(() => {setLoading(false); })

  }

  


  return (
    <>
  

      <form onSubmit={handleSubmit(submitForm)} className="position-relative">
        {loading && <div className="position-absolute top-0 start-0 w-100 h-100 bg-light opacity-50 rounded ">

          </div>}
      <h1>{ formData.name || 'Loading form...' }</h1>
      <p>{ formData.desc || "Loading description..." }</p>
      { state === EFormState.READY &&
        error === null && 
        <>
          {
          questions.map(q => {
            return (
              <div key={q.id} className="pb-1">
                <Question {...q} register={register} errors={errors} key={q.id} readonly={readOnly} />
              </div>
            )
          })}
          {!readOnly && <button type="submit" className="btn btn-primary">{ loading ? (<><span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          <span className="visually-hidden">Loading...</span></>) : (isEditing ? "Save" : "Submit")}</button>}
          <small className="ms-2 text-secondary">{ (formData.allowsMultipleSubmissions && `You've submitted this form ${ prevSubmissions.length } times.`) || (readOnly ? 'You have already submitted this form and cannot edit it!' : `You may only submit this form once! ${formData.allowsEditingSubmissions && '(You can edit it later!)'}`)}</small>
        </>
      }
      { state === EFormState.LOADING && "Loading form..."}
      { state === EFormState.SUBMITTED && 
        <div className="alert alert-success">
          Your response has been recorded! (ID: {recentSubmission?.id}) { formData.allowsMultipleSubmissions && <a href="#" onClick={() => {reset(); setState(EFormState.READY)}} className="alert-link">Submit again</a> }
        </div>
      }
      { error && 
        <div className="alert alert-danger">
          Oops, something went wrong! <a href="#" onClick={() => {setError(null); setState(EFormState.READY)}} className="alert-link">Try again</a>
        </div>
      }


      
    </form>
    

    </>
  )
}


export const Question: FC<IAnswerableQuestion> = ({ ...props }) => {


  const [hasFormHook, setHasFormHook] = useState<boolean>(props.register !== undefined)

  

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
        <div className="d-flex justify-content-between align-items-end ">
          <label htmlFor={`form-question-${props.id}`} className="form-label">{ props.name }</label>

          { props.required && <p className="text-end mt-0 mb-0 text-danger" style={{'fontSize': '.8rem'}}>Required *</p>}
        </div>


        {
          hasFormHook && props.register && props.errors ? 
          <input {...props.register(props.id, { required: props.required, minLength: props.type_data?.min, maxLength: props.type_data?.max })} readOnly={props.readonly || false} type={props.type} placeholder={props.type_data?.placeholder} className={"form-control " + (props.errors[props.id] && "is-invalid")} id={`form-question-${props.id}`} onKeyPress={e => e.key === 'Enter' && e.preventDefault()} aria-describedby="emailHelp"  />
          :
          <input type={props.type} placeholder={props.type_data?.placeholder} className="form-control" id={`form-question-${props.id}`} onKeyPress={e => e.key === 'Enter' && e.preventDefault()} aria-describedby="emailHelp" required={props.required} />
        }
        
        <div id={`form-question-${props.id}-help`} className="form-text">{ props.desc }</div>
      </div>
    )
  }

  return null
}

export const CheckboxQuestion: FC<IAnswerableQuestion> = ({ ...props }) => {

  const [hasFormHook, setHasFormHook] = useState<boolean>(props.register !== undefined)

  return (
    <div className="mb-3">
          <div className="d-flex justify-content-between align-items-end">
          <label htmlFor={`form-question-${props.id}`} className="form-label">{ props.name }</label>

          { props.required && <p className="text-end mt-0 mb-0 text-danger" style={{'fontSize': '.8rem'}}>Required *</p>}
        </div>
        {hasFormHook ? <div>
          { props.type_data?.options?.map(option => {
            if (!props.register) return
            if (!props.errors) return
            return (
              <div key={option.value} className="form-check form-check-inline">
                <input {...props.register(props.id, { required: true })} disabled={props.readonly || false}  className={"form-check-input " + (props.errors[props.id] && "is-invalid")} type="checkbox" id={`form-question-${props.id}-option-${option.key}`} value={option.value} />
                <label className="form-check-label" htmlFor={`form-question-${props.id}-option-${option.key}`}>{option.key}</label>
              </div>
            )
          })}
        </div>
        :
        <div>
          { props.type_data?.options?.map(option => {
            return (
              <div key={option.value} className="form-check form-check-inline">
                <input className={"form-check-input "} type="checkbox" id={`form-question-${props.id}-option-${option.key}`} value={option.value} />
                <label className="form-check-label" htmlFor={`form-question-${props.id}-option-${option.key}`}>{option.key}</label>
              </div>
            )
          })}
        </div>
        }



        <div id={`form-question-${props.id}-help`} className="form-text">{ props.desc }</div>
      </div>
  )
}

export const RadioQuestion: FC<IAnswerableQuestion> = ({ ...props }) => {

  const [hasFormHook, setHasFormHook] = useState<boolean>(props.register !== undefined)

  return (
    <div className="mb-3">
  <div className="d-flex justify-content-between align-items-end">
          <label htmlFor={`form-question-${props.id}`} className="form-label">{ props.name }</label>

          { props.required && <p className="text-end mt-0 mb-0 text-danger" style={{'fontSize': '.8rem'}}>Required *</p>}
        </div>
    { hasFormHook ? 
    <div>
      { props.type_data?.options?.map(option => {
        if (!props.register) return
        if (!props.errors) return
        return (
          <div key={option.value} className="form-check form-check-inline">
            <input {...props.register(props.id, { required: true })} disabled={props.readonly || false}  className={"form-check-input " + (props.errors[props.id] && "is-invalid")} type="radio" name={props.id} id={`form-question-${props.id}-option-${option.key}`} value={option.value} />
            <label className="form-check-label" htmlFor={`form-question-${props.id}-option-${option.key}`}>{option.key}</label>
          </div>
        )
      })}
    </div>
    :
    <div>
      { props.type_data?.options?.map(option => {
        return (
          <div key={option.value} className="form-check form-check-inline">
            <input  className={"form-check-input " } type="radio" name={props.id} id={`form-question-${props.id}-option-${option.key}`} value={option.value} />
            <label className="form-check-label" htmlFor={`form-question-${props.id}-option-${option.key}`}>{option.key}</label>
          </div>
        )
      })}
    </div>
    }


    <div id={`form-question-${props.id}-help`} className="form-text">{ props.desc }</div>
  </div>
  )
}

export const SelectQuestion: FC<IAnswerableQuestion> = ({ ...props }) => {

  const [hasFormHook, setHasFormHook] = useState<boolean>(props.register !== undefined)

  return (
    <div className="mb-3">
  <div className="d-flex justify-content-between align-items-end">
          <label htmlFor={`form-question-${props.id}`} className="form-label">{ props.name }</label>

          { props.required && <p className="text-end mt-0 mb-0 text-danger" style={{'fontSize': '.8rem'}}>Required *</p>}
        </div>
    
    {
      hasFormHook && props.register && props.errors ?
      <select {...props.register(props.id, { required: true, validate: v => v !== "default_none" })} disabled={props.readonly || false}  className={"form-select " + ((props.errors[props.id] && "is-invalid"))} defaultValue="default_none" id={`form-question-${props.id}`} aria-label="Default select example" >
      <option value="default_none">Open this select menu</option>
      {
        props.type_data?.options?.map(option => {
          return (
            <option key={option.value} value={option.value}>{option.key}</option>
          )
        })
      }
    </select>
    :
    <select className="form-select" defaultValue="default_none" id={`form-question-${props.id}`} aria-label="Default select example" required={props.required}>
      <option value="default_none">Open this select menu</option>
      {
        props.type_data?.options?.map(option => {
          return (
            <option key={option.value} value={option.value}>{option.key}</option>
          )
        })
      }
    </select>
    }


    <div id={`form-question-${props.id}-help`} className="form-text">{ props.desc }</div>
  </div>
  )
}

export const TextareaQuestion: FC<IAnswerableQuestion> = ({ ...props }) => {


  const [hasFormHook, setHasFormHook] = useState<boolean>(props.register !== undefined)


  return (
    <div className="mb-3">
  <div className="d-flex justify-content-between align-items-end">
          <label htmlFor={`form-question-${props.id}`} className="form-label">{ props.name }</label>

          { props.required && <p className="text-end mt-0 mb-0 text-danger" style={{'fontSize': '.8rem'}}>Required *</p>}
        </div>

      {
        hasFormHook && props.register && props.errors ? 
        <textarea {...props.register(props.id, { required: props.required })} readOnly={props.readonly || false}  id={`form-question-${props.id}`} rows={3} className={"form-control " + (props.errors[props.id] && "is-invalid")}></textarea>
        :
        <textarea id={`form-question-${props.id}`} rows={3} className="form-control"></textarea>
      }
    


    <div id={`form-question-${props.id}-help`} className="form-text">{ props.desc }</div>
  </div>
  )
}

export const RangeQuestion: FC<IAnswerableQuestion> = ({ ...props }) => {

  const [hasFormHook, setHasFormHook] = useState<boolean>(props.register !== undefined)

 

  const calcSteps = () => {

    if ((props.type_data?.step || 0) < 0) return

    let steps: number = (((props.type_data?.max || 100) + 1 - (props.type_data?.min || 0))) / (props.type_data?.step || 10);
    return Math.round(steps);
  }

  return (
    <div className="mb-3 pb-3">
      <div className="d-flex justify-content-between align-items-end">
        <label htmlFor={`form-question-${props.id}`} className="form-label">{ props.name }</label>

        { props.required && <p className="text-end mt-0 mb-0 text-danger" style={{'fontSize': '.8rem'}}>Required *</p>}
      </div>

      
      {
        hasFormHook && props.register && props.errors ?
        <input {...props.register(props.id, { required: props.required })} disabled={props.readonly || false}  defaultValue={(props.type_data?.max || 2)/2 || 0} type={props.type} placeholder={props.type_data?.placeholder} min={props.type_data?.min} max={props.type_data?.max} step={props.type_data?.step} className="form-range" style={{padding: '0'}} id={`form-question-${props.id}`}  aria-describedby="emailHelp" required={props.required} />
        :
        <input defaultValue={(props.type_data?.max || 2)/2 || 0} type={props.type} placeholder={props.type_data?.placeholder} min={props.type_data?.min} max={props.type_data?.max} step={props.type_data?.step} className="form-range" style={{padding: '0'}} id={`form-question-${props.id}`}  aria-describedby="emailHelp" required={props.required} />
      }

      <div className="d-flex justify-content-between position-relative mb-3" style={{marginLeft: "7px", marginRight: "7px"}}>
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

const formRVs: HTMLCollectionOf<Element> = document.getElementsByTagName('custom-form-result-viewer')


for (let i = 0; i < forms.length; i++) {
  let form = forms.item(i)
  ReactDOM.render(<FeedbackFormViewer id={form?.getAttribute('form-id') || 'no-id'} />, form);
}

for (let i = 0; i < formBuilders.length; i++) {
  let form = formBuilders.item(i)
  ReactDOM.render(<FormBuilder />, form);
}

for (let i = 0; i < formRVs.length; i++) {
  let form = formRVs.item(i)
  ReactDOM.render(<ResultViewer id={form?.getAttribute('form-id') || 'no-id'} />, form);
}