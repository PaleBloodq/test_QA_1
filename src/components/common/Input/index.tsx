import { useDispatch } from "react-redux"

type Props = {
    value: string,
    setValue: (arg: string) => void,
    placeholder: string,
    type: string,
}


export default function Input({ value, setValue, placeholder, type }: Props) {
    const dispatch = useDispatch()
    return (
        <div className="w-full h-[50px] custom-border px-[22px] flex justify-between items-center mb-3">
            <input className="w-full text-subtitle-info bg-transparent outline-none" placeholder={placeholder} type={type} value={value} onChange={(e) => dispatch(setValue(e.target.value))} />
        </div>
    )
}
