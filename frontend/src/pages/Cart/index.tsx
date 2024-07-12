import { useDispatch, useSelector } from "react-redux";
import Container from "../../components/common/Container";
import { userSelector } from "../../features/User/userSelectors";
import Order from "./Order";
import Tag from "../../components/common/Tag";
import CheckBox from "../../components/common/CheckBox";
import { useEffect, useState } from "react";
import CartItem from "./CartItem";
import { useGetCartQuery, useRemoveFromCartMutation } from "../../services/cartApi";
import { cartSelector } from "../../features/Cart/cartSelectors";
import { setCartItems } from "../../features/Cart/cartSlice";

export default function Cart() {
    const dispatch = useDispatch();
    const { userData } = useSelector(userSelector);
    const [useCashback, setUseCashback] = useState(false);
    const { totalPrice, totalCashback, items } = useSelector(cartSelector);

    const { data: cartData, isLoading, isError, refetch } = useGetCartQuery({});
    const [removeFromCart, { data: afterRemoveData }] = useRemoveFromCartMutation();

    useEffect(() => {
        if (cartData) {
            dispatch(setCartItems(cartData))
        }
    }, [cartData])

    useEffect(() => {
        if (afterRemoveData) {
            dispatch(setCartItems(afterRemoveData))
        }
    }, [afterRemoveData])

    useEffect(() => {
        refetch()
    }, [])


    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (isError) {
        return <div>Error loading cart data</div>;
    }

    return (
        <Container>
            <h1 className="text-header">Корзина</h1>
            <div className="mt-7 flex flex-col gap-2 w-full">
                {items.map((item) => (
                    <CartItem onRemove={(id) => removeFromCart({ id: id })} key={item.id} item={item} />
                ))}
                {items.length === 0 && <h1 className="text-title">Корзина пуста</h1>}
            </div>
            <div className="mt-8 custom-border w-full flex flex-col gap-2 px-[35px] py-[21px]">
                <p className="text-subtitle">Итого:</p>
                <div className="flex gap-5 items-center">
                    <h1 className="price-medium ">{Math.round(totalPrice).toLocaleString()} ₽</h1>
                    <Tag type="cashback">Кэшбэк: {Math.round(totalCashback)} ₽</Tag>
                </div>
                <div className="flex w-full justify-between items-center">
                    <CheckBox onClick={() => setUseCashback(!useCashback)} checked={useCashback}>Списать баллы</CheckBox>
                    <div className="flex gap-2">
                        <p className="text-subtitle-info">У вас:</p>
                        <Tag type="discount">{userData?.cashback || 0} ₽</Tag>
                    </div>
                </div>
            </div>
            <Order useCashback={useCashback} />
        </Container>
    );
}