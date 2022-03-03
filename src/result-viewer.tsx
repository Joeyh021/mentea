import axios from "axios";
import React, { useEffect } from "react";
import { FC, useState } from "react";
import { useForm } from "react-hook-form";
import { EFormState, IAnswer, IFeedbackForm, IFeedbackFormProps, IQuestion, IStoredSubmission, ISubmission, Question } from ".";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";




const ResultViewer: FC<IFeedbackFormProps> = ({ id }) => {
    const [loading, setLoading] = useState<boolean>(false)

    const [questions, setQuestions] = useState<IQuestion[]>([])
  
    const [formData, setFormData] = useState<IFeedbackForm>({id: 'Loading...', name: 'Loading Form Name...', desc: "", allowsEditingSubmissions: false, allowsMultipleSubmissions: true, acceptingSubmissionsUntil: null})

    const [state, setState] = useState<EFormState>(EFormState.LOADING)
    const [error, setError] = useState<string | null>(null)

    const { register, handleSubmit, formState: { errors }, reset, setValue } = useForm()

    const [current, setCurrent] = useState<number>(0)
    const [submissions, setSubmissions] = useState<IStoredSubmission[]>([])

    const nextSubmission = () => {
        if (current >= submissions.length-1) return
        setCurrent(current+1)
    }

    const prevSubmission = () => {
        if (current === 0) return

        setCurrent(current - 1)
    }

    useEffect(() => {

       
        if (state !== EFormState.READY || submissions.length === 0) return
          // Load submission here
    
          axios.get(`/feedback-api/submission/${submissions[current].id}`).then(res => {
            let ans: IAnswer[] = []
    
            let data: [] = res.data.answers
            data.forEach((d: {associated_question: string, data: any}) => {
              ans.push({a: d.data, q: d.associated_question})
            })
    
            ans.forEach(a => setValue(a.q, a.a))
          })
    
          
        
      }, [current,state, submissions])

      useEffect(() => {
        loadFormFromId(id)
      }, [id])

      const loadFormFromId = (formId :string) => {

    

        axios.get(`/feedback-api/${formId}/`).then(res => {
          setFormData({...res.data.formData, id: formId})
          setQuestions(res.data.questions)

            gatherSubmissions(formId)

          

          
        }).catch(e => {
          setError("No form was found with the given ID, or it could not be loaded!")
        })
    
        
      }

      const gatherSubmissions = (formId: string) => {
          axios.get(`/feedback-api/${formId}/submissions/`).then(res => {
              setSubmissions(res.data.submissions)
              setState(EFormState.READY)
          })
      }

      if (submissions.length === 0 && state === EFormState.READY) {
          return (
              <div className="alert alert-danger">There is <strong>no feedback</strong> available for this workshop yet</div>
          )
      }

      if (state !== EFormState.READY || submissions.length === 0) {
        return "Loading results..."
      }

    return (
        <>
  

        <div className="position-relative">

        <h1>{ formData.name || 'Loading form...' } - Results</h1>
        <p>{ formData.desc || "Loading description..." }</p>
        <h2>Submission: { submissions[current]?.id || "No submissions" }</h2>
        <button className={"btn me-2 " + (current === 0 ? "btn-secondary pe-none " : "btn-primary")} onClick={prevSubmission}>Previous</button>
        <button className={"btn " + (current === submissions.length-1 || submissions.length == 0 ? "btn-secondary pe-none " : "btn-primary")} onClick={nextSubmission}>Next</button>
        { state === EFormState.READY &&
          error === null && 
          <>
            {
            questions.map(q => {
              return (
                <div key={q.id} className="pb-1">
                  <Question {...q} register={register} errors={errors}  key={q.id} readonly={true} />
                </div>
              )
            })}

          </>
        }
        { state === EFormState.LOADING && "Loading form..."}

        { error && 
          <div className="alert alert-danger">
            Oops, something went wrong! <a href="#" onClick={() => {setError(null); setState(EFormState.READY)}} className="alert-link">Try again</a>
          </div>
        }
  
  
        
      </div>
      
  
      </>
    )
}

export default ResultViewer