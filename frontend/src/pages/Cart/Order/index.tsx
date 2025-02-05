import SelectType from "./SelectType";
import { cartSelector } from "../../../features/Cart/cartSelectors";
import Input from "../../../components/common/Input";
import { useDispatch, useSelector } from "react-redux";
import { clearCart, setAccountEmail, setAccountPassword, setHasAccount, setPromocode, setReciptEmail, setRememberData, setTotalCashback } from "../../../features/Cart/cartSlice";
import CheckBox from "../../../components/common/CheckBox";
import { useEffect, useState } from "react";
import Button from "../../../components/common/Button";
import { useCheckPromocodeMutation, useMakeOrderMutation } from "../../../services/userApi";
import { userSelector } from "../../../features/User/userSelectors";
import { setTotalPrice } from "../../../features/Cart/cartSlice";
import calcTotalPrice from "../../../helpers/calcTotalPrice";
import calcOrderCashback from "../../../helpers/calcOrderCashback";

export default function Order({ useCashback }: { useCashback: boolean }) {


    const { hasAccount, accountEmail, accountPassword, reciptEmail, rememberData, promocode, items } = useSelector(cartSelector)
    const [makeOrder, { data: orderData, error: orderErorr }] = useMakeOrderMutation();
    const [checkPromocode, { data: promoData, error: promoError }] = useCheckPromocodeMutation();
    const [sameEmail, setSameEmail] = useState(false)
    const dispatch = useDispatch()

    const { userData } = useSelector(userSelector)

    useEffect(() => {
        sameEmail ? dispatch(setReciptEmail(accountEmail)) : dispatch(setReciptEmail(""))
    }, [sameEmail])

    const orderObject = {
        // cart: items?.map((item) => { return { id: item.id, type: item.product_type } }),
        spendCashback: useCashback,
        hasAccount: hasAccount,
        accountEmail: hasAccount ? accountEmail : null,
        accountPassword: hasAccount ? accountPassword : null,
        billEmail: reciptEmail,
        promoCode: promocode,
        rememberAccount: rememberData
    }

    function handleOrder() {
        if (orderObject.billEmail) {
            makeOrder(orderObject)
            dispatch(clearCart())
        }
    }

    function checkIsValidPromo() {
        if (promocode) {
            checkPromocode({ promoCode: promocode })
        }
    }

    useEffect(() => {
        if (orderData?.PaymentUrl) {
            dispatch(clearCart())
            window.location.href = orderData?.PaymentUrl
        }
    }, [orderData])


    useEffect(() => {
        if (orderErorr || promoError) {
            window.Telegram.WebApp.showAlert('Произошла ошибка! Попробуйте еще раз или перезайдите в приложение.');
        }
    }, [orderErorr, promoError])


    useEffect(() => {
        dispatch(setTotalPrice(calcTotalPrice(items, (promoData?.result === true && promoData?.discount), (useCashback ? userData.cashback : 0))))
    }, [items, promoData, useCashback])

    useEffect(() => {
        dispatch(setTotalCashback(calcOrderCashback(items, (promoData?.result === true ? promoData?.discount : 0))))
    }, [items, promoData])


    return (
        <div className="mt-8">
            <h1 className="text-title-xl mb-5">Куда оформить заказ?</h1>
            <SelectType hasAccount={hasAccount} setHasAccount={setHasAccount} />
            <div className="w-full mt-7">
                {hasAccount
                    ? (
                        <>
                            <h1 className="text-title-xl mb-5">Оформление заказа:</h1>
                            <Input value={accountEmail} setValue={setAccountEmail} placeholder="Введите E-mail от аккаунта" type="email" />
                            <Input value={accountPassword} setValue={setAccountPassword} placeholder="Введите пароль от аккаунта" type="password" />
                            <div className="mt-6 mb-4">
                                <CheckBox onClick={() => setSameEmail(!sameEmail)} checked={sameEmail}>E-mail для чека такой же, как логин</CheckBox>
                            </div>
                        </>
                    )
                    : (<></>)}
                <Input value={reciptEmail} setValue={setReciptEmail} placeholder="Введите E-mail для чека" type="email" />
                <div className="mt-6">
                    <CheckBox checked={rememberData} onClick={() => dispatch(setRememberData(!rememberData))}>Запомнить данные для следующих заказов</CheckBox>
                </div>
                <div className="flex w-full mt-6 items-start flex-col">
                    <div className="flex w-full gap-2">
                        <Input placeholder="Ввести промокод" value={promocode} setValue={setPromocode} type='text' />
                        <button onClick={checkIsValidPromo} className="mb-3">
                            <svg width="50" height="50" viewBox="0 0 50 50" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect width="50" height="50" rx="8" fill="#B13430" />
                                <path d="M32.4632 24.3939L26.4632 18.3939C26.1284 18.0591 25.5857 18.0591 25.251 18.3939C24.942 18.7029 24.9182 19.1891 25.1797 19.5253L25.251 19.6061L29.7879 24.1428H18.1428C17.7032 24.1428 17.3409 24.4737 17.2914 24.9L17.2856 25C17.2856 25.4395 17.6165 25.8018 18.0428 25.8513L18.1428 25.8571H29.7879L25.251 30.3939C24.942 30.7029 24.9182 31.1891 25.1797 31.5253L25.251 31.6061C25.56 31.915 26.0462 31.9388 26.3824 31.6774L26.4632 31.6061L32.4632 25.6061L32.5459 25.5102L32.6074 25.4149L32.6532 25.3183L32.6835 25.228L32.7048 25.1272L32.7108 25.0765L32.7141 24.9835L32.7108 24.9235L32.6969 24.8279L32.6716 24.7324L32.6339 24.6372L32.5891 24.5536L32.5318 24.4713C32.5105 24.4441 32.4876 24.4183 32.4632 24.3939L26.4632 18.3939L32.4632 24.3939Z" fill="white" />
                            </svg>
                        </button>
                    </div>
                    {promoData ? promoData?.result === true ? <span className="text-sm text-green-600">Промокод применен. Скидка составила <strong>{promoData?.discount}%</strong></span> : <span className="text-sm text-red-600">Такого промокода не существует</span> : <></>}
                </div>
                <Button onClick={handleOrder}>Оформить заказ</Button>
            </div>
        </div>
    )
}
