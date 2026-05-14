
import ContactCard from "./ContactCard"
import { useSelector } from "react-redux";
import Pagination from "./Paginator";

export default function ContactList() {
    const contacts = useSelector((state) => state.contacts.contacts)
    const searchQuery = useSelector((state) => state.contacts.searchQuery)
    const totalLength = useSelector((state) => state.contacts.total)

    function CreateCardsFromData(contracts) {
        return contracts.map((d) => <ContactCard name={d.name} email={d.email} phone={d.phone} key={d.id} id={d.id} />)
    }

    return (
        <div className="container mx-auto flex flex-col">
            <div className="my-3 w-[100%] flex flex-row justify-around gap-4 mx-auto">
                <span>Найдено контактов: {totalLength}</span>
                <span></span>
            </div>
            <div className="flex flex-col gap-4 items-center">
                {CreateCardsFromData(contacts)}
                <Pagination currentPage={1} totalPages={10}/>
            </div>
        </div>

    )
}