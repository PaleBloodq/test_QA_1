import { useSelector } from "react-redux";
import Container from "../../components/common/Container";
import { cartSelector } from "../../features/Cart/cartSelectors";
import { CartItemType } from "../../types/cartItem";
import CartItem from "./CartItem";
import { useEffect, useState } from "react";
import { getDiscount } from "../../hooks/getDiscount";
import Tag from "../../components/common/Tag";
import CheckBox from "../../components/common/CheckBox";
import { userSelector } from "../../features/User/userSelectors";

export default function Cart() {

    function calculateTotalPrice(cartItems: CartItemType[]): number {
        let totalPrice = 0;
        for (const item of cartItems) {
            const discountPrice = getDiscount(item.price, item.discount);
            totalPrice += discountPrice;
        }
        return totalPrice;
    }

    function calculateTotalCashback(cartItems: CartItemType[]): number {
        let totalCashback = 0;
        for (const item of cartItems) {
            const cashback = item.cashback;
            totalCashback += cashback;
        }
        return totalCashback;
    }

    const { items }: { items: CartItemType[] } = useSelector(cartSelector)

    const [totalPrice, setTotalPrice] = useState(0)
    const [totalCashback, setTotalCashback] = useState(0)
    const [useCashback, setUseCashback] = useState(false)

    const { userData } = useSelector(userSelector)

    useEffect(() => {
        setTotalPrice(calculateTotalPrice(items))
        setTotalCashback(calculateTotalCashback(items))
    }, [items])

    useEffect(() => {
        useCashback === true ? setTotalPrice(totalPrice - userData.cashback) : setTotalPrice(calculateTotalPrice(items))
    }, [useCashback])

    return (
        <Container>
            <h1 className="text-header">Корзина</h1>
            <div className="mt-7 flex flex-col gap-2 w-full">
                {items.map((item: CartItemType) => {
                    return (
                        <CartItem key={item.id} item={item} />
                    )
                })}
                {items.length === 0 && <h1 className="text-title">Корзина пуста</h1>}
            </div>
            <div className="mt-8 custom-border w-full flex flex-col gap-2 px-[35px] py-[21px]">
                <p className="text-subtitle">Итого:</p>
                <div className="flex gap-5 items-center">
                    <h1 className="price-medium ">{totalPrice.toLocaleString()} ₽</h1>
                    <Tag type="cashback">Кэшбек: {totalCashback} ₽</Tag>
                </div>
                <div className="flex w-full justify-between items-center">
                    <CheckBox onClick={() => setUseCashback(!useCashback)} checked={useCashback}>Списать баллы</CheckBox>
                    <div className="flex gap-2">
                        <p className="text-subtitle-info">У вас:</p>
                        <Tag type="discount">{userData?.cashback || 0} ₽</Tag>
                    </div>
                </div>
            </div>
        </Container>
    )
}
