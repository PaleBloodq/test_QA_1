import { useDispatch, useSelector } from "react-redux";
import { searchValue } from "../../../features/Search/searchSelectors"
import { setSearchValue } from "../../../features/Search/searchSlice";

export default function Search() {
    const dispatch = useDispatch();

    const inputValue = useSelector(searchValue);

    return (
        <div className="w-full flex items-center px-5 gap-3  custom-border">
            <svg className="fill-secondary-light dark:fill-secondary-dark" width="15" height="15" viewBox="0 0 15 15" xmlns="http://www.w3.org/2000/svg">
                <path d="M7.93524 0.123722C8.32287 0.143309 8.64637 0.364354 9.0089 0.470679C9.76185 0.694521 10.3949 1.10024 11.0084 1.60668C12.0542 2.46568 12.6565 3.5709 13.0386 4.81043C13.574 6.54241 13.3398 8.22123 12.5282 9.8301C12.4055 10.0735 12.1852 10.2414 12.0737 10.5044C11.9872 10.7115 11.9649 10.815 12.1295 10.9773C12.9772 11.8083 13.7999 12.6617 14.6588 13.4787C14.96 13.7669 15.066 14.0915 14.96 14.4468C14.8457 14.8246 14.4776 14.9561 14.115 14.9981C13.9198 15.0204 13.7915 14.8442 13.6632 14.7155C12.9967 14.0495 12.333 13.3808 11.6693 12.7149C11.463 12.5078 11.2482 12.312 11.053 12.0993C10.8969 11.9258 10.7463 11.9202 10.5678 12.0489C9.53597 12.81 8.35355 13.2101 7.09863 13.322C6.3401 13.3892 5.55927 13.3276 4.83421 13.0282C4.5386 12.9051 4.22069 12.8576 3.92788 12.7177C2.2686 11.9258 1.14754 10.6499 0.455939 8.95431C0.210533 8.35274 0.151968 7.72598 0.048786 7.09922C-0.0683396 6.37732 0.0404216 5.69181 0.21611 5.00909C0.433629 4.15848 0.801737 3.36384 1.33438 2.66434C1.95626 1.85011 2.68411 1.17019 3.62669 0.708511C4.63899 0.213259 5.69034 -0.0133808 6.80303 0.000609351C7.1572 0.00620541 7.50857 0.0845502 7.86553 0.064964C7.87389 0.104136 7.89063 0.134915 7.93804 0.120925L7.93524 0.123722ZM1.91164 5.08743C1.85587 5.20215 1.77221 5.30568 1.81404 5.44838C1.73595 5.72258 1.65508 5.99399 1.65508 6.28219C1.66066 6.58718 1.66902 6.88936 1.6746 7.19435C1.70249 7.32866 1.73316 7.46016 1.76105 7.59447C1.88097 7.79313 1.78336 8.04775 1.91722 8.24361C1.96463 8.30797 1.8977 8.41429 1.99809 8.45906C2.24908 9.1082 2.5893 9.70418 3.10521 10.1798C3.17771 10.2414 3.25301 10.303 3.32551 10.3645C3.5012 10.5688 3.71593 10.7227 3.95855 10.8374C4.01154 10.9101 4.08404 10.9493 4.17049 10.9717C4.19559 11.0277 4.243 11.0416 4.29877 11.0444C4.39917 11.148 4.51908 11.2151 4.65852 11.2431C4.75891 11.3298 4.8593 11.411 5.00432 11.3942C5.24414 11.5201 5.51744 11.5229 5.774 11.5845C6.05287 11.6068 6.33174 11.632 6.61061 11.6544C6.70264 11.6544 6.79745 11.6544 6.88948 11.6544C6.98151 11.6544 7.07632 11.6544 7.16835 11.6544C7.46395 11.5621 7.79023 11.6012 8.07747 11.4641C8.59617 11.3718 9.0563 11.1508 9.46903 10.8318C9.51923 10.7954 9.57222 10.759 9.62241 10.7227C10.1774 10.3253 10.6375 9.83289 10.9805 9.24811C11.3012 8.70249 11.5634 8.1233 11.6219 7.47415C11.6247 7.38182 11.6303 7.28948 11.6331 7.19435C11.7502 7.06844 11.6861 6.91735 11.6888 6.77465C11.739 6.53401 11.6582 6.30737 11.6191 6.07514C11.6498 5.80653 11.6693 5.54071 11.4908 5.30568C11.4574 5.10702 11.3988 4.91675 11.3152 4.73488C11.2901 4.60897 11.2482 4.49145 11.1674 4.38792C11.1088 4.19766 11.014 4.02698 10.8773 3.88428C10.8634 3.80034 10.816 3.73878 10.7463 3.69121C10.6989 3.57649 10.6236 3.48136 10.5204 3.40861C10.2945 3.09243 10.0184 2.82662 9.69213 2.61397C9.64193 2.5776 9.59174 2.54402 9.54154 2.50765C9.4523 2.44329 9.36306 2.37894 9.27382 2.31738C9.19295 2.23624 9.09535 2.18028 8.9838 2.15789C8.95591 2.10193 8.90571 2.08794 8.84994 2.09074C8.70771 1.96483 8.52366 1.95923 8.35355 1.91446C8.33961 1.89488 8.32008 1.88928 8.30056 1.90047C8.22806 1.87529 8.15276 1.85011 8.08026 1.82772C7.72051 1.69342 7.35519 1.5843 6.96478 1.61787C6.77793 1.61787 6.59388 1.61787 6.40703 1.61787C6.18115 1.69622 5.92738 1.61507 5.70707 1.73819C5.51744 1.74938 5.32502 1.7158 5.15212 1.82493C4.25137 2.15789 3.44822 2.63356 2.84586 3.40302C2.70642 3.51494 2.59208 3.64924 2.514 3.81153C2.37178 4.01858 2.23234 4.22564 2.15426 4.46907C2.01761 4.65374 1.96184 4.86919 1.91443 5.08743H1.91164Z" />
            </svg>
            <input onChange={(e) => dispatch(setSearchValue(e.target.value))} value={inputValue} className="w-full bg-transparent outline-none text-secondary-light dark:text-secondary-dark" type="text" placeholder="Найти игру..." />
        </div>
    )
}
