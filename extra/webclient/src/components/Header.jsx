import Searchbar from "./SearchBar";

export default function Header({ onAddClick }) {
    return (
        <div className="drawer">
            <div className="drawer-content flex flex-col">
                <div className="navbar bg-base-300">
                    <div className="w-full max-w-7xl mx-auto px-4 lg:px-8">
                        <div className="flex items-center justify-between w-full">

                            <div className="font-bold text-lg md:text-xl">
                                Список контактов
                            </div>

                            <Searchbar/>

                            <button
                                className="btn btn-primary"
                                onClick={() => { onAddClick() }}
                            >
                                Добавить контакт
                            </button>

                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
}