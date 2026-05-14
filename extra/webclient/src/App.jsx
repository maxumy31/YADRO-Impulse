import { useEffect, useState } from 'react'

import './global.css'
import ContactList from './components/ContactList'
import Header from './components/Header'
import AddContactModal from './components/AddContactModal'
import { getUsers } from './api/api'
import { useDispatch, useSelector } from 'react-redux'
import { loadData } from './store/contactsSlice'

function App() {

	const dispatch = useDispatch();
	const searchQuery = useSelector((state) => state.contacts.searchQuery);
	const currentPage = useSelector((state) => state.contacts.currentPage);

	const [isModalOpened, setModalOpen] = useState(false);
	const pageSize = 10;

	(
		async () => {
			const users = await getUsers(currentPage,pageSize,searchQuery);
			dispatch(loadData(users));
		}
	)();

	return (
		<div>
			<Header onAddClick={() => {
				setModalOpen(true);
			}} />
			<ContactList />
			<AddContactModal isOpen={isModalOpened} onClose={() => setModalOpen(false)} />
		</div>
	)
}

export default App
