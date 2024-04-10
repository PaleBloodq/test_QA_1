import Slider from 'rc-slider';
import './slider.styles.css'
import { searchSelector } from "../../../features/Search/searchSelectors";
import { useDispatch, useSelector } from "react-redux";
import { setSearchHighPrice, setSearchLowPrice } from "../../../features/Search/searchSlice";
import { memo, useEffect } from 'react';
import { FilterInitData } from '../../../types/filterInitData';

const PriceSlider = memo(({ initData }: { initData: FilterInitData }) => {

    const dispatch = useDispatch()
    const { lowPrice, highPrice } = useSelector(searchSelector)

    useEffect(() => {
        highPrice === 0 && dispatch(setSearchHighPrice(initData.highPrice));
    }, [])

    const handleRangeChange = (value: number[] | number) => {
        if (Array.isArray(value)) {
            dispatch(setSearchLowPrice(value[0]));
            dispatch(setSearchHighPrice(value[1]));
        }
    }
    return (
        <>
            <div className="flex gap-[10px] w-full">
                <div className="w-[168px] h-[50px] custom-border flex px-5 gap-2 items-center">
                    <p className="text-subtitle">От:</p>
                    <input onChange={(e) => Number(e.target.value) > (initData.lowPrice - 1) ? dispatch(setSearchLowPrice(Number(e.target.value))) : dispatch(setSearchLowPrice(initData.lowPrice))} value={lowPrice} className="w-full bg-transparent outline-none text-subtitle-info" type="number" />
                </div>
                <div className="w-[168px] h-[50px] custom-border flex px-5 gap-2 items-center">
                    <p className="text-subtitle">До:</p>
                    <input onChange={(e) => Number(e.target.value) < initData.highPrice ? dispatch(setSearchHighPrice(Number(e.target.value))) : dispatch(setSearchHighPrice(initData.highPrice))} value={highPrice} className="w-full bg-transparent outline-none text-subtitle-info" type="number" />
                </div>
            </div>
            <div className="w-full flex justify-center">
                <Slider allowCross={false} min={initData.lowPrice} max={initData.highPrice} value={[lowPrice, highPrice]} onChange={(value) => handleRangeChange(value)} step={100} range />
            </div>
        </>
    )
})

export default PriceSlider