import { useDispatch, useSelector } from "react-redux";
import SvgIcon from "./SvgIcon";
import { setPage } from "../store/contactsSlice";

export default function Pagination() {

  const dispatch = useDispatch();
  const currentPage = useSelector((state) => state.contacts.currentPage)
  const totalPages = useSelector((state) =>
    Math.ceil(state.contacts.total / state.contacts.pageSize)
  )

  const MAX_VISIBLE = 10;

  let startPage = Math.max(1, currentPage - Math.floor(MAX_VISIBLE / 2));
  let endPage = startPage + MAX_VISIBLE - 1;

  if (endPage > totalPages) {
    endPage = totalPages;
    startPage = Math.max(1, endPage - MAX_VISIBLE + 1);
  }

  const pages = [];
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }

  function onPageChange(newPage) {
    dispatch(setPage(newPage));
  }

  return (
    <>
      {pages.length > 0
        &&
        <div className="ring-1 ring-base-300 p-4 flex flex-row rounded-lg w-fit gap-2 items-center justify-center card card-dash">

          <div className="flex flex-row gap-2">
            {pages.map((page) => (
              <button
                key={page}
                className={`btn btn-ghost min-w-[2rem] ${page === currentPage ? "bg-primary text-white" : ""
                  }`}
                onClick={() => onPageChange(page)}
              >
                {page}
              </button>
            ))}
          </div>
        </div>
      }
    </>
  );
}