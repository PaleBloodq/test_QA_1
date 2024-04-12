import { useRef, useState } from "react"
import { useDispatch } from "react-redux"

type Props = {
    value: string,
    setValue: (arg: string) => void,
    placeholder: string,
    type: string,
    hardlyEditable?: boolean,
    localValue?: boolean
}


export default function Input({ value, setValue, placeholder, type, hardlyEditable, localValue }: Props) {
    const ref = useRef<HTMLInputElement>(null)
    const dispatch = useDispatch()
    const [isEditable, setIsEditable] = useState(hardlyEditable)
    return (
        <div className="w-full h-[50px] custom-border px-[22px] flex justify-between items-center mb-3">
            <input ref={ref} readOnly={isEditable ? isEditable : false} className="w-full text-subtitle-info bg-transparent outline-none" placeholder={placeholder} type={type} value={value} onChange={(e) => !localValue ? dispatch(setValue(e.target.value)) : setValue(e.target.value)} />
            {hardlyEditable &&
                <button onClick={() => { setIsEditable(!isEditable); ref.current && ref.current.focus() }} className="w-6 h-6">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M15.8012 3.0633L16.9339 4.196C17.7707 5.03284 17.7707 6.38962 16.9339 7.22646L15.0002 9.16011L7.24764 16.9127C6.64485 17.5155 5.82731 17.8541 4.97486 17.8541H3.60735C2.79865 17.8541 2.14307 17.1985 2.14307 16.3898V15.0224C2.14307 14.1698 2.48174 13.3522 3.08457 12.7494L10.8374 4.9971L10.837 4.99694L12.7707 3.0633C13.6075 2.22646 14.9643 2.22646 15.8012 3.0633ZM11.7859 6.06885L4.0947 13.7596C3.75979 14.0945 3.57164 14.5487 3.57164 15.0224V16.3898C3.57164 16.4095 3.58763 16.4255 3.60735 16.4255H4.97486C5.44844 16.4255 5.90263 16.2374 6.23751 15.9025L13.9288 8.2117L11.7859 6.06885ZM13.7808 4.07345L12.8574 4.99694L15.0002 7.1398L15.9237 6.21631C16.2027 5.93736 16.2027 5.4851 15.9237 5.20615L14.791 4.07345C14.5121 3.7945 14.0598 3.7945 13.7808 4.07345Z" fill="#606D7B" />
                    </svg>
                </button>
            }
        </div>
    )
}
