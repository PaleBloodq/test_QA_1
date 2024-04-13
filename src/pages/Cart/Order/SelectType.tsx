import { useDispatch } from "react-redux"

export default function SelectType({ hasAccount, setHasAccount }: { hasAccount: boolean, setHasAccount: (arg: boolean) => any }) {

    const dispatch = useDispatch()

    return (
        <>
            <div className="w-full flex gap-3">
                <button onClick={() => dispatch(setHasAccount(true))} className={`w-full h-[33px] text-[14px] ${hasAccount ? "rounded-lg red-gradient font-bold text-white" : "rounded-lg border dark:border-[#FFFFFF1A] text-[#606D7B] dark:text-[#FFFFFF99]"}`} >
                    На мой аккаунт
                </button>
                <button onClick={() => dispatch(setHasAccount(false))} className={`w-full h-[33px] text-[14px] ${!hasAccount ? "rounded-lg red-gradient font-bold text-white" : "rounded-lg border dark:border-[#FFFFFF1A] text-[#606D7B] dark:text-[#FFFFFF99]"}`} >
                    У меня нет аккаунта
                </button>
            </div>
            <h1 className="text-subtitle mt-4">{hasAccount ? 'У меня есть турецкий аккаунт, оформите на него' : 'Бот бесплатно создаст для вас турецкий аккаунт, оформит на него заказ и передаст вам логин с паролем'}</h1>
        </>
    )
}
