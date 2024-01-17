import { kreamTableRawDataProps, KreamTable } from "./table/kream-table";
import SearchBar from "../searchBar";

const Main = async ({ kreamProductCardList }: { kreamProductCardList: kreamTableRawDataProps[] }) => {
    return (
        <div className="py-4 flex-center flex-col ">
            <div className="py-8">
                <SearchBar />
            </div>
            <KreamTable tableData={kreamProductCardList} />
        </div>
    );
};

export default Main;
