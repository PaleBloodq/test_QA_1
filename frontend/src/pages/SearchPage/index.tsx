import { useDispatch, useSelector } from "react-redux";
import Container from "../../components/common/Container";
import { searchSelector } from "../../features/Search/searchSelectors";
import { setSearchValue } from "../../features/Search/searchSlice";
import { useGetSearchFiltersQuery, useGetSearchProductsMutation } from "../../services/productsApi";
import { useEffect, useState } from "react";
import Filter from "./Filter";
import SearchItem from "./SearchItem";

export default function SearchPage() {

    const dispatch = useDispatch();
    const { value, languages, limit, maxPrice, minPrice, offset, platforms } = useSelector(searchSelector);
    const [showFilter, setShowFilter] = useState(false)

    const [getSearchProducts, { data, isLoading, error }] = useGetSearchProductsMutation();
    const { data: filterData } = useGetSearchFiltersQuery({})
    const params = {
        minPrice: minPrice,
        maxPrice: maxPrice,
        platforms: platforms,
        languages: languages,
        limit: limit,
        q: value
    }
    useEffect(() => {
        getSearchProducts({ params })
    }, [])

    console.log(data)



    return (
        <Container>
            {showFilter && <Filter getSearchProducts={getSearchProducts} setShowFilter={setShowFilter} initData={filterData} />}
            {!showFilter &&
                <div className="w-full flex flex-col">
                    <div className="w-full h-[38px] flex items-center justify-between">
                        <input
                            onBlur={() => getSearchProducts({ params })}
                            onKeyDown={(event) => event.key === "Enter" && getSearchProducts({ params })}
                            onChange={(e) => dispatch(setSearchValue(e.target.value))} value={value}
                            className="w-full bg-transparent outline-none text-header" type="text" placeholder="Найти игру..."
                        />
                        <button
                            onClick={() => getSearchProducts({ params })}
                            className="w-[38px] h-[38px] rounded-xl bg-[#f6f7fa] border border-[#e7e7e8] dark:border-none dark:bg-[#FFFFFF0D] flex flex-shrink-0 items-center justify-center mx-2"
                        >
                            <svg
                                width={24}
                                height={24}
                                viewBox="0 0 24 24"
                                xmlns="http://www.w3.org/2000/svg"
                                className="w-6 h-6 fill-[#606D7B] dark:fill-[#C35530]"
                                preserveAspectRatio="xMidYMid meet"
                            >
                                <path
                                    d="M11.1429 3.85718C15.1667 3.85718 18.4286 7.1191 18.4286 11.1429C18.4286 12.846 17.8442 14.4127 16.865 15.6532L20.749 19.5368C21.0837 19.8715 21.0837 20.4142 20.749 20.749C20.4142 21.0837 19.8715 21.0837 19.5368 20.749L15.6532 16.865C14.4127 17.8442 12.846 18.4286 11.1429 18.4286C7.1191 18.4286 3.85718 15.1667 3.85718 11.1429C3.85718 7.1191 7.1191 3.85718 11.1429 3.85718ZM11.1429 5.57146C8.06588 5.57146 5.57146 8.06588 5.57146 11.1429C5.57146 14.2199 8.06588 16.7143 11.1429 16.7143C14.2199 16.7143 16.7143 14.2199 16.7143 11.1429C16.7143 8.06588 14.2199 5.57146 11.1429 5.57146Z"
                                />
                            </svg>
                        </button>
                        <button onClick={() => setShowFilter(true)} className="w-[38px] h-[38px] rounded-xl bg-[#f6f7fa] border border-[#e7e7e8] dark:border-none dark:bg-[#FFFFFF0D] flex flex-shrink-0 items-center justify-center">
                            <svg className="w-6 h-6 fill-[#606D7B] dark:fill-[#C35530]" width="24" height="24" viewBox="0 0 24 24"
                                xmlns="http://www.w3.org/2000/svg">
                                <path d="M15.8571 12.8571C17.2162 12.8571 18.3642 13.7608 18.7329 15.0001L20.5714 15C21.0448 15 21.4286 15.3837 21.4286 15.8571C21.4286 16.3305 21.0448 16.7143 20.5714 16.7143L18.7327 16.715C18.3636 17.9538 17.2159 18.8571 15.8571 18.8571C14.4984 18.8571 13.3506 17.9538 12.9816 16.715L3.42855 16.7143C2.95517 16.7143 2.57141 16.3305 2.57141 15.8571C2.57141 15.3837 2.95517 15 3.42855 15L12.9813 15.0001C13.3501 13.7608 14.4981 12.8571 15.8571 12.8571ZM15.8571 14.3571C15.0287 14.3571 14.3571 15.0287 14.3571 15.8571C14.3571 16.6855 15.0287 17.3571 15.8571 17.3571C16.6856 17.3571 17.3571 16.6855 17.3571 15.8571C17.3571 15.0287 16.6856 14.3571 15.8571 14.3571ZM8.99998 5.14282C10.359 5.14282 11.507 6.04654 11.8758 7.28582L20.5714 7.28568C21.0448 7.28568 21.4286 7.66944 21.4286 8.14282C21.4286 8.61621 21.0448 8.99997 20.5714 8.99997L11.8755 9.00068C11.5065 10.2395 10.3587 11.1428 8.99998 11.1428C7.64124 11.1428 6.49347 10.2395 6.12443 9.00068L3.42855 8.99997C2.95517 8.99997 2.57141 8.61621 2.57141 8.14282C2.57141 7.66944 2.95517 7.28568 3.42855 7.28568L6.12417 7.28582C6.49294 6.04654 7.64092 5.14282 8.99998 5.14282ZM8.99998 6.64282C8.17156 6.64282 7.49998 7.3144 7.49998 8.14282C7.49998 8.97125 8.17156 9.64282 8.99998 9.64282C9.82841 9.64282 10.5 8.97125 10.5 8.14282C10.5 7.3144 9.82841 6.64282 8.99998 6.64282Z" />
                            </svg>
                        </button>
                    </div>
                    {!isLoading &&
                        <div className="w-full flex flex-wrap mt-10 gap-y-[40px] gap-x-[15px]">
                            {data?.map((item: any, index: number) => <SearchItem key={index} item={item} />)}
                        </div>
                    }
                </div>
            }
        </Container>
    )
}