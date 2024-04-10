import CheckField from "./CheckField";
import 'rc-slider/assets/index.css';
import { setSearchLanguages, setSearchPlatforms } from "../../../features/Search/searchSlice";
import { useDispatch, useSelector } from "react-redux";
import Button from "../../../components/common/Button";
import PriceSlider from "./PriceSlider";
import { FilterInitData } from "../../../types/filterInitData";
import { searchSelector } from "../../../features/Search/searchSelectors";

type FilterPropsType = {
    initData: FilterInitData,
    setShowFilter: (value: boolean) => void,

}

export default function Filter({ initData, setShowFilter }: FilterPropsType) {

    const dispatch = useDispatch();

    const { platforms, languages } = useSelector(searchSelector)

    return (
        <div className="absoulte top-0 left-0 w-full h-full">
            <div className="w-full flex justify-between items-center mb-7">
                <h1 className="text-title text-[24px]">Фильтры</h1>
                <button onClick={() => setShowFilter(false)} className="w-[38px] h-[38px] rounded-xl bg-[#f6f7fa] border border-[#e7e7e8] dark:border-none dark:bg-[#FFFFFF0D] flex flex-shrink-0 items-center justify-center mx-2">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M5.39387 5.39387C5.72861 5.05914 6.27132 5.05914 6.60606 5.39387L12 10.7871L17.3939 5.39387C17.7029 5.08489 18.1891 5.06112 18.5253 5.32257L18.6061 5.39387C18.9408 5.72861 18.9408 6.27132 18.6061 6.60606L13.2128 12L18.6061 17.3939C18.915 17.7029 18.9388 18.1891 18.6774 18.5253L18.6061 18.6061C18.2713 18.9408 17.7286 18.9408 17.3939 18.6061L12 13.2128L6.60606 18.6061C6.29707 18.915 5.81087 18.9388 5.47462 18.6774L5.39387 18.6061C5.05914 18.2713 5.05914 17.7286 5.39387 17.3939L10.7871 12L5.39387 6.60606C5.08489 6.29707 5.06112 5.81087 5.32257 5.47462L5.39387 5.39387Z" fill="#606D7B" />
                    </svg>
                </button>
            </div>
            <div>
                <h3 className="text-subtitle block mb-4">Платформа</h3>
                <div className="flex gap-[10px]">
                    {initData.platforms.map((platform: string, index: number) => <button key={'platform-' + index} onClick={() => dispatch(setSearchPlatforms(platform))}><CheckField defaultChecked={platforms.includes(platform)}>{platform}</CheckField></button>)}
                </div>
            </div>
            <div className="mt-7">
                <h3 className="text-subtitle block mb-4">Язык</h3>
                <div className="flex gap-[10px]">
                    {initData.languages.map((lang: string, index: number) => <button key={'language-' + index} onClick={() => dispatch(setSearchLanguages(lang))}><CheckField defaultChecked={languages.includes(lang)}>{lang}</CheckField></button>)}
                </div>
            </div>
            <div className="mt-7">
                <h3 className="text-subtitle block mb-4">Цена</h3>
                <div className="flex flex-col gap-4">
                    <PriceSlider initData={initData} />
                    <div className="w-full mt-[100px]">
                        <Button onClick={() => setShowFilter(false)}>Применить фильтры</Button>
                    </div>
                </div>
            </div>
        </div>
    )
}