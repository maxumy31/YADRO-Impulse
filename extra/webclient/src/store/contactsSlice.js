import { createSlice } from '@reduxjs/toolkit';
import { createUser, deleteUser, getUsers } from '../api/api';


const initialState = {
  contacts: [],
  total: 0,
  searchQuery: "",
  currentPage: 1,
  pageSize: 10,
};

const contactsSlice = createSlice({
  name: 'contacts',
  initialState,
  reducers: {

    addContact: {
      prepare: (id, name, email, phone) => ({
        payload: {
          id: id,
          name,
          email,
          phone,
        },
      }),

      reducer: (state, action) => {
        createUser(action.payload);

        getUsers(state.currentPage, state.pageSize, state.searchQuery)
          .then(users => loadData(users));
      },
    },

    removeContact(state, action) {
      deleteUser(action.payload);

      getUsers(state.currentPage, state.pageSize, state.searchQuery)
        .then(users => loadData(users));
    },

    setSearchQuery(state, action) {
      state.searchQuery = action.payload;
      state.currentPage = 1;
    },

    loadData(state, action) {
      state.total = action.payload.total;
      state.contacts = action.payload.users;
    },

    setPage(state, action) {
      state.currentPage = action.payload;
    }
  },
});

export const { addContact, removeContact, setSearchQuery, loadData, setPage } = contactsSlice.actions;
export default contactsSlice.reducer;