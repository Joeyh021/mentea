import { randomUUID } from "crypto"
import React, { useState } from "react"
import { FC } from "react"
import { IQuestion, IQuestionTypeData, Question } from "."
import { v4 as uuidv4 } from 'uuid';
import axios from "axios";
import { readSync } from "fs";

interface IQuestionType {
    htmlName: string
    visualName: string
}

const questionTypes: IQuestionType[] = [
    {
        htmlName: "text",
        visualName: "Short Text"
    },
    {
        htmlName: "textarea",
        visualName: "Long Text"
    },
    {
        htmlName: "number",
        visualName: "Number"
    },
    {
        htmlName: "email",
        visualName: "Email"
    },
    {
        htmlName: "password",
        visualName: "Sensitive / Password"
    },
    {
        htmlName: "radio",
        visualName: "Multiple Choice"
    },
    {
        htmlName: "checkbox",
        visualName: "Checkbox"
    },
    {
        htmlName: "select",
        visualName: "Select"
    },
    {
        htmlName: "range",
        visualName: "Slider / Range"
    }
]

interface IFormEditorData {
    id: string
    name: string
    desc: string
}

interface IJSONFormBuilder {
    formData: IFormEditorData
    questions: IQuestion[]
}

interface IFormBuilder {
    defaultMode?: EFormBuilderMode
}

enum EFormBuilderMode {
    CREATE, EDIT
}

const FormBuilder: FC<IFormBuilder> = ({ defaultMode  }) => {

    const [mode, setMode] = useState<EFormBuilderMode>(defaultMode || EFormBuilderMode.CREATE)

    const [formData, setFormData] = useState<IFormEditorData>({
        id: "new-form",
        name: "",
        desc: ""
    })
    const [questions, setQuestions] = useState<IQuestion[]>([])

    const deleteQuestion = (id: string) => {


        let newState: IQuestion[] = []

        questions.forEach(s => {
            if (s.id !== id){
                newState.push(s)
            }
        })

        setQuestions(newState)

    }

    const addQuestion = () => {
        let id: string = uuidv4()
        setQuestions([...questions, {
            id: id,
            name: `A new question`,
            type: "text",
            required: false
        }])
    }

    const updateQuestion = (q: IQuestion) => {
        
        let newState: IQuestion[] = []

        questions.forEach(s => {
            if (s.id === q.id){
                newState.push(q)
            } else {
                newState.push(s)
            }
        })

        setQuestions(newState)
    }

    const convertJSONToForm = (json: string) => {
        try {
            let fromJSON: IJSONFormBuilder = JSON.parse(json);

            setFormData(fromJSON.formData)
            setQuestions(fromJSON.questions || [])
        } catch (e) {
            alert('Unable to parse form')
        }
    }

    const convertResponseToForm = (json: any, id: string) => {
        try {
            let fromJSON: IJSONFormBuilder = json;

            setFormData({...fromJSON.formData, id: id})
            setQuestions(fromJSON.questions || [])

            setMode(EFormBuilderMode.EDIT)
        } catch (e) {
            alert('Unable to parse form')
        }
    }

    const convertFormToJSON = () => {
        let toJson: IJSONFormBuilder = {
            formData: formData,
            questions: questions
        }

        return JSON.stringify(toJson)
    }

    const convertFormToObj = () => {
        let toObj: IJSONFormBuilder = {
            formData: formData,
            questions: questions
        }

        return toObj
    }

    const saveForm = () => {
        let data = convertFormToObj()

        let fd: FormData = new FormData()
        fd.append('jsonData', JSON.stringify(data))

        if (mode === EFormBuilderMode.CREATE){
            axios.post('/feedback-api/create/', fd).then(res => {
                console.log(res.data)
                let json = res.data

                if (json.result === 'success') {
                    console.log(json.data)
                    setFormData({...formData, id: json.data.formId})

                    let updatedQuestions: IQuestion[] = []
                    let counter = 0
                    questions.forEach(q => {
                        q.id = json.data.questionIds[counter]
                        counter = counter + 1
                        updatedQuestions.push(q)
                    })

                    setQuestions(updatedQuestions)
                    setMode(EFormBuilderMode.EDIT)
                }

            })
        } else {
            axios.post('/feedback-api/editor-edit/', fd).then(r => console.log(r.data))
        }

    }

    const loadFormFromId = () => {

        let formId: string = prompt("Form ID") || ""

        axios.get(`/feedback-api/${formId}/`).then(res => convertResponseToForm(res.data, formId))

        
    }
    

    return (
        <div>
            
            <h1>Form Builder: { formData.name || "Give me a name!"}</h1>

            <div className="row g-2 mb-2">
                <div className="col-6">
                  
                    <div className="form-floating">
                            <input type="text" className="form-control" id={`form-editor-${formData.id}-basesettings-name`} placeholder="Name" defaultValue={formData.name} onKeyUp={(e) => {setFormData({...formData, name: e.target.value})}} onKeyPress={e => e.key === 'Enter' && e.preventDefault()}/>
                            <label htmlFor={`form-editor-${formData.id}-basesettings-name`}>Name</label>
                        </div>
                </div>
               
            </div>
            <div className="row mb-3">
                <div className="col-12">
                <div className="form-floating">
                        <textarea className="form-control" style={{height: '100px'}} id={`form-editor-${formData.id}-basesettings-desc`} placeholder="Name" defaultValue={formData.desc} onKeyUp={(e) => {setFormData({...formData, desc: e.target.value})}} />
                        <label htmlFor={`form-editor-${formData.id}-basesettings-desc`}>Description</label>
                    </div>
                </div>
            </div>

            <div className="row border-bottom mb-4">
                <div className="col-6">
                    <h2>Editor</h2>
                </div>
                <div className="col-6">
                    <h2>Preview</h2>
                </div>
            </div>

            <div className="row border-bottom mb-2">
                <div className="col-6">
                    <h5>Title & Description Preview:</h5>
                </div>
                <div className="col-6">
                    <h3>{ formData.name || 'Give me a name!' }</h3>
                    <p>{ formData.desc || "Give me a description above! (If you leave it blank then I won't show up when actually used!)" }</p>
                </div>
            </div>
            {
                questions.map((q) => {
                    return (
                        <div key={q.id} className="row mb-2 mt-2 ">
                            <div className="col-6 d-flex flex-column justify-items-center pe-5">
                                <div className="row g-3 align-items-center mb-3">
                                    <div className="col-auto">
                                        <label htmlFor={`form-editor-${formData.id}-question-${q.id}-name`} className="col-form-label">Name: </label>
                                    </div>
                                    <div className="col-auto  ">
                                        <input type="text" id={`form-editor-${formData.id}-question-${q.id}-name`} defaultValue={q.name} className="form-control" onKeyUp={(e) => {updateQuestion({...q, name: e.target.value});}} onKeyPress={e => e.key === 'Enter' && e.preventDefault()} aria-describedby="passwordHelpInline" />
                                    </div>
                                    <div className="col-auto ms-auto">
                                        <button className="btn btn-danger" type="button" onClick={() => deleteQuestion(q.id)}>Delete</button>
                                    </div>
                                </div>

                               

                                


                                    <div className="accordion" id={`form-editor-${formData.id}-question-${q.id}-accord`}>
                                        <div className="accordion-item">
                                            <h2 className="accordion-header" id={`form-editor-${formData.id}-question-${q.id}-settings`}>
                                                <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target={`#form-editor-${formData.id}-question-${q.id}-settings-content`} aria-expanded="false" aria-controls="collapseOne">
                                                    Question Settings
                                                </button>
                                            </h2>
                                            <div id={`form-editor-${formData.id}-question-${q.id}-settings-content`} className="accordion-collapse collapse" aria-labelledby={`form-editor-${formData.id}-question-${q.id}-settings`} data-bs-parent={`#form-editor-${formData.id}-question-${q.id}-accord`}>
                                                <div className="accordion-body">
                                                <div className="row g-3 align-items-center mb-2">
                                                    <div className="col-auto">
                                                        <label htmlFor={`form-editor-${formData.id}-question-${q.id}-typr`} className="col-form-label">Type: </label>
                                                    </div>
                                                    <div className="col-auto  ">
                                                        <select id={`form-editor-${formData.id}-question-${q.id}-type`} className="form-select" onChange={(e) => updateQuestion({...q, type: e.target.value})} aria-describedby="passwordHelpInline" >
                                                            {
                                                                questionTypes.map(qt => {
                                                                    return (
                                                                        <option key={qt.htmlName} value={qt.htmlName}>{ qt.visualName }</option>
                                                                    )
                                                                })
                                                            }
                                                        </select>
                                                    </div>
                                                </div>
                                                <div className="row">
                                                    <div className="col">
                                                        <div className="form-check">
                                                            <input className="form-check-input" type="checkbox" value="" checked={q.required} onChange={() => updateQuestion({...q, required: !q.required})} id={`form-editor-${formData.id}-question-${q.id}-req`} />
                                                            <label className="form-check-label" style={{fontSize: '1rem'}} htmlFor={`form-editor-${formData.id}-question-${q.id}-req`}>
                                                                Required
                                                            </label>
                                                        </div>
                                                    </div>
                                                    
                                                </div>

                                                  
                                                </div>
                                            </div>
                                        </div>
                                        {
                                    (q.type === "checkbox" || q.type === "radio" || q.type === "select") &&
                                        <div className="accordion-item">
                                            <h2 className="accordion-header" id={`form-editor-${formData.id}-question-${q.id}-settingsOpt`}>
                                                <button className="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target={`#form-editor-${formData.id}-question-${q.id}-settingsOpt-content`} aria-expanded="true" aria-controls="collapseOne">
                                                    Option Settings
                                                </button>
                                            </h2>
                                            <div id={`form-editor-${formData.id}-question-${q.id}-settingsOpt-content`} className="accordion-collapse collapse" aria-labelledby={`form-editor-${formData.id}-question-${q.id}-settingsOpt`} data-bs-parent={`#form-editor-${formData.id}-question-${q.id}-accord`}>
                                                <div className="accordion-body">
                                                    <div className="row g-3 align-items-center">
                                                        <div className="col">
                                
                                                            <div className="row">
                                                                <div className="col-auto">
                                                                    <label htmlFor={`form-editor-${formData.id}-question-${q.id}-addoption`} className="col-form-label">Add option: </label>
                                                                </div>
                                                                <div className="col-auto">
                                                                    <input type="text" id={`form-editor-${formData.id}-question-${q.id}-addoption`} className="form-control" onKeyPress={(e) => {if (e.key === 'Enter') { updateQuestion({...q, type_data: {...q.type_data, options: [...q.type_data?.options || [], {key: e.target.value, value: uuidv4()}]}}); e.target.value=""; e.preventDefault()}}} />
                                                                </div>
                                                                
                                                            </div>
                                                            <div className="row">
                                                            {
                                                                q.type_data?.options?.map(opt => {
                                                                    return (
                                                                        <div key={opt.value} className="col-auto d-flex me-2" onClick={() => updateQuestion({...q, type_data: {...q.type_data, options: [...q.type_data?.options?.filter(o => o.value !== opt.value) || []]}}) }>
                                                                            <p className="me-2">{ opt.key }</p>
                                                                            <span className="btn-close"></span>
                                                                        </div>
                                                                        
                                                                    )
                                                                })
                                                            }
                                                   
                                                            </div>
                                                            
                                                        </div>

                                                    </div>
                                                </div>
                                            </div>
                                        </div>}


                                    {q.type === "range" && 
                                        <div className="accordion-item">
                                            <h2 className="accordion-header" id={`form-editor-${formData.id}-question-${q.id}-rangeOpt`}>
                                                <button className="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target={`#form-editor-${formData.id}-question-${q.id}-rangeOpt-content`} aria-expanded="true" aria-controls="collapseOne">
                                                    Slider / Range Settings
                                                </button>
                                            </h2>
                                            <div id={`form-editor-${formData.id}-question-${q.id}-rangeOpt-content`} className="accordion-collapse collapse" aria-labelledby={`form-editor-${formData.id}-question-${q.id}-rangeOpt`} data-bs-parent={`#form-editor-${formData.id}-question-${q.id}-accord`}>
                                                <div className="accordion-body">
                                                    <div className="row g-3 align-items-center">
                                                        <div className="col">
                                
                                                            <div className="row mb-2">
                                                                <div className="col-sm-1">
                                                                    <label htmlFor={`form-editor-${formData.id}-question-${q.id}-rangemin`} className="col-form-label">Min: </label>
                                                                </div>
                                                                <div className="col-auto">
                                                                    <input type="number" id={`form-editor-${formData.id}-question-${q.id}-rangemin`} className="form-control" onChange={(e) => updateQuestion({...q, type_data: {...q.type_data, min: Number.parseInt(e.target.value) || 0}})}  />
                                                                </div>
                                                                
                                                            </div>
                                                            <div className="row mb-2">
                                                                <div className="col-sm-1">
                                                                    <label htmlFor={`form-editor-${formData.id}-question-${q.id}-rangemin`} className="col-form-label">Max: </label>
                                                                </div>
                                                                <div className="col-auto">
                                                                    <input type="number" id={`form-editor-${formData.id}-question-${q.id}-rangemin`} className="form-control" onChange={(e) => updateQuestion({...q, type_data: {...q.type_data, max: Number.parseInt(e.target.value) || 100}})}  />
                                                                </div>
                                                                
                                                            </div>
                                                            <div className="row mb-2">
                                                                <div className="col-sm-1">
                                                                    <label htmlFor={`form-editor-${formData.id}-question-${q.id}-rangemin`} className="col-form-label">Step: </label>
                                                                </div>
                                                                <div className="col-auto">
                                                                    <input type="number" id={`form-editor-${formData.id}-question-${q.id}-rangemin`} className="form-control" onChange={(e) => updateQuestion({...q, type_data: {...q.type_data, step: Number.parseInt(e.target.value) || 1}})}   />
                                                                </div>
                                                                
                                                            </div>
                                          
                                                            
                                                        </div>

                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    }
                                    </div>

                                    
                                
                                
                            </div>
                            <div className="col-6 ps-5">
                                <Question {...q} />
                            </div>
                            <hr className="mt-4" />
                        </div>
                    )
                })
            }
            <button className="btn btn-primary me-2" type="button" onClick={addQuestion}>Add Question</button>
            <button className="btn btn-primary me-2" type="button" onClick={saveForm}>{ mode === EFormBuilderMode.CREATE ? "Save Form" : "Update Form"}</button>
            <button className="btn btn-info " type="button" onClick={loadFormFromId}>Load custom form</button>
        </div>
    )
}

export default FormBuilder


  