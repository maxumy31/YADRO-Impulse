import { useDispatch } from "react-redux";
import { setSearchQuery } from "../store/contactsSlice";

export default function Searchbar() {
    const dispatch = useDispatch()
    
    return(<>
            <input type="text" placeholder="Фильтрация по имени" className="input" 
                onChange={(e) => dispatch(setSearchQuery(e.target.value))}/>
        </>);
}