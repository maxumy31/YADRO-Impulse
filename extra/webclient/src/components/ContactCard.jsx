import { useDispatch } from "react-redux";
import { removeContact } from "../store/contactsSlice";
import SvgIcon from "./SvgIcon";

export default function ContactCard({ id, name, phone, email }) {
  const dispatch = useDispatch();

  return (
    <div className="ring-1 ring-base-300 p-4 rounded-lg w-full max-w-[900px] grid grid-cols-[1fr_1fr_1.4fr_0.4fr] gap-4 items-center card card-dash">

      <div className="flex items-center gap-3 min-w-0">
        <SvgIcon name="account_circle_icon" className="w-6 h-6 text-primary shrink-0" />
        <span className="truncate">{name}</span>
      </div>

      <div className="flex items-center gap-2 min-w-0">
        <SvgIcon name="phone_icon" className="w-5 h-5 text-primary shrink-0" />
        <span className="truncate">{phone}</span>
      </div>


      <div className="flex items-center gap-2 min-w-0">
        <SvgIcon name="mail_icon" className="w-5 h-5 text-primary shrink-0" />
        <span className="truncate">{email}</span>
      </div>

      <div className="flex justify-end sm:justify-center">
        <button
          className="btn btn-ghost shrink-0"
          onClick={() => dispatch(removeContact(id))}
        >
          <SvgIcon name="trash_icon" className="w-6 h-6 text-primary" />
        </button>
      </div>

    </div>
  );
}