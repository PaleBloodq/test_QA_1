import { useState } from "react"
import { getDiscount } from "../../../hooks/getDiscount"

export default function SelectPrice({ price, discount }: { price: number, discount: number }) {

    const discountPrice = getDiscount(price, discount)

    type PsPlusState = 'withPsPlus' | 'noPsPlus';

    const [selected, setSelected] = useState<PsPlusState>('withPsPlus');


    return (
        <div className='w-full flex gap-3 mb-4'>
            <button onClick={() => setSelected('withPsPlus')} className={`w-full h-20 flex flex-col items-center justify-center gap-1 ${selected === 'withPsPlus' ? 'custom-border__psPlus' : 'custom-border'}`}>
                <div className="flex items-center gap-1">
                    <svg className="fill-[#ffb800]" width="13" height="13" viewBox="0 0 13 13" xmlns="http://www.w3.org/2000/svg">
                        <path fillRule="evenodd" clipRule="evenodd" d="M4.33333 1C4.33333 0.447715 4.78105 0 5.33333 0H7.66667C8.21895 0 8.66667 0.447715 8.66667 1V3.33333C8.66667 3.88562 9.11438 4.33333 9.66667 4.33333H12C12.5523 4.33333 13 4.78105 13 5.33333V7.66667C13 8.21895 12.5523 8.66667 12 8.66667H9.66667C9.11438 8.66667 8.66667 9.11438 8.66667 9.66667V12C8.66667 12.5523 8.21895 13 7.66667 13H5.33333C4.78105 13 4.33333 12.5523 4.33333 12V9.66667C4.33333 9.11438 3.88562 8.66667 3.33333 8.66667H1C0.447715 8.66667 0 8.21895 0 7.66667V5.33333C0 4.78105 0.447715 4.33333 1 4.33333H3.33333C3.88562 4.33333 4.33333 3.88562 4.33333 3.33333V1Z" />
                    </svg>
                    <span className="text-[14px] text-[#3c67d7] dark:text-[#ffb800]">с PS Plus</span>
                </div>
                <div className="flex items-center gap-2">
                    <h1 className="price-small">{discountPrice} ₽</h1>
                    <div className="flex justify-center items-center min-w-[42px] rounded-[6px] h-[22px] text-white font-bold bg-[#3C67D7] dark:bg-[#ffb800] text-[14px]">-{discount}%</div>
                </div>
            </button>
            <button onClick={() => setSelected('noPsPlus')} className={`w-full h-20 flex flex-col items-center justify-center gap-1 ${selected === 'noPsPlus' ? 'custom-border__psPlus' : 'custom-border'}`}>
                <div className="flex items-center gap-1">
                    <span className="text-[14px] text-subtitle">без PS Plus</span>
                </div>
                <div className="flex items-center gap-2">
                    <h1 className="price-small">{price} ₽</h1>
                </div>
            </button>
        </div>
    )
}
