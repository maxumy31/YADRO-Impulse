import { useEffect, useRef } from "react"
import { useDispatch } from "react-redux"
import { addContact } from "../store/contactsSlice"
import { nanoid } from "@reduxjs/toolkit"

export default function AddContactModal({ isOpen, onClose }) {
    const dialogRef = useRef(null)
    const formRef = useRef(null)

    const nameInput = useRef(null)
    const emailInput = useRef(null)
    const phoneInput = useRef(null)

    const dispatch = useDispatch()

    useEffect(() => {
        if (isOpen) {
            dialogRef.current.showModal()
        } else {
            dialogRef.current.close()
        }
    }, [isOpen])


    function takeInputFromForm() {
        const form = formRef.current
        if (!form) return

        if (form.checkValidity()) {
            const name = nameInput.current.value;
            const email = emailInput.current.value;
            const phone = phoneInput.current.value;
            return { name: name, email: email, phone: phone }
        }
        else {
            return null
        }
    }


    function addNewContact() {
        const input = takeInputFromForm()
        if (!input) return
        dispatch(addContact(nanoid(), input.name, input.email, input.phone))
        onClose()
    }

    return (<>
        <dialog ref={dialogRef} className="modal">
            <form onSubmit={(e) => e.preventDefault()} ref={formRef}>
                <div className="modal-box flex flex-col">
                    <div className="flex flex-row justify-around items-center">
                        <h3 className="font-bold text-lg">Добавить новый контакт</h3>
                        <button className="btn btn-outline " onClick={onClose}>
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" className="size-4"><path d="M5.28 4.22a.75.75 0 0 0-1.06 1.06L6.94 8l-2.72 2.72a.75.75 0 1 0 1.06 1.06L8 9.06l2.72 2.72a.75.75 0 1 0 1.06-1.06L9.06 8l2.72-2.72a.75.75 0 0 0-1.06-1.06L8 6.94 5.28 4.22Z" /></svg>
                        </button>
                    </div>
                    <div className="flex flex-col gap-4 items-center my-8">
                        <input type="text" className="input" placeholder="Name" ref={nameInput} required />
                        <input type="email" className="input" placeholder="email@example.com" pattern="^.+@.+\..{2,}$" required ref={emailInput} />
                        <input type="tel" className="input" placeholder="79999999999" pattern="^\[0-9]{5,15}$" required ref={phoneInput} />
                    </div>

                    <div className="flex flex-row justify-center">
                        <button className="btn btn-primary mt-4 w-[80%]"
                            onClick={() => addNewContact()}>
                            Добавить контакт
                        </button>
                    </div>
                </div>
            </form>
        </dialog>
    </>)
}