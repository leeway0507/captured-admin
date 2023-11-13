import { kreamTableRawDataProps } from "./table/type";
import SearchBar from "../searchBar";
import { KreamTable } from "./table/table";

const Main = async ({ kreamProductCardList }: { kreamProductCardList: kreamTableRawDataProps[] }) => {
    return (
        <div className="py-4">
            <div className="py-8">
                <SearchBar />
            </div>
            <KreamTable tableData={kreamProductCardList} />
        </div>
    );
};

export default Main;
