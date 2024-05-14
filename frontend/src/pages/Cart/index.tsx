import { useDispatch, useSelector } from "react-redux";
import Container from "../../components/common/Container";
import { cartSelector } from "../../features/Cart/cartSelectors";
import { CartItemType } from "../../types/cartItem";
import CartItem from "./CartItem";
import { useEffect, useState } from "react";
import { getDiscount } from "../../hooks/getDiscount";
import Tag from "../../components/common/Tag";
import CheckBox from "../../components/common/CheckBox";
import { userSelector } from "../../features/User/userSelectors";
import Order from "./Order";
import calcCashback from "../../helpers/calcCashback";
import axios from "axios";
import { addToCart, setTotalPrice } from "../../features/Cart/cartSlice";

export default function Cart() {

    const { isLoggined } = useSelector(userSelector)
    const dispatch = useDispatch()


    const checkItem = async (item: CartItemType) => {
        try {
            const response = await axios.get(`https://chatlabs.site/aokibot/backend/api/publication/${item.id}`);
            return response.status === 200;
        } catch (error) {
            console.error(error);
            return false;
        }
    };

    function calcStartPrice(cartItems: CartItemType[]): number {
        return cartItems.reduce((total, { final_price }) => total + final_price, 0);
    }

    function calculateTotalCashback(cartItems: CartItemType[]): number {
        return cartItems.reduce((total, item) => total + calcCashback(item.price, item.cashback), 0);
    }

    const { items, totalPrice }: { items: CartItemType[], totalPrice: number } = useSelector(cartSelector)

    const [totalCashback, setTotalCashback] = useState(0)
    const [useCashback, setUseCashback] = useState(false)

    const { userData } = useSelector(userSelector)

    useEffect(() => {
        dispatch(setTotalPrice(calcStartPrice(items)))
        setTotalCashback(calculateTotalCashback(items))
    }, [items])

    // useEffect(() => {
    //     let newTotalPrice = calculateTotalPrice(items);
    //     if (isLoggined && useCashback) {
    //         const cashbackLimit = userData.cashback;
    //         if (newTotalPrice < cashbackLimit) {
    //             newTotalPrice = 0;
    //         } else {
    //             newTotalPrice -= cashbackLimit;
    //         }
    //     }
    //     setTotalPrice(newTotalPrice);
    // }, [isLoggined, useCashback, items, userData]);

    // useEffect(() => {
    //     if (useCashback) {
    //         setTotalPrice(totalPrice - userData?.cashback)
    //     } else if (!useCashback) {
    //         setTotalPrice(totalPrice + userData?.cashback)
    //     }
    // }, [useCashback])

    useEffect(() => {
        if (items.length === 0) {
            const storageParsedItems: CartItemType[] | null = JSON.parse(localStorage.getItem('storageCartItems'));
            storageParsedItems?.forEach((item) => dispatch(addToCart(item)));
        }
    }, [items, dispatch]);


    useEffect(() => {
        const fetchItems = async () => {
            try {
                const storageParsedItems: CartItemType[] = JSON.parse(localStorage.getItem('storageCartItems')) || [];
                const promises = storageParsedItems.map(item => checkItem(item));
                const results = await Promise.all(promises);
                const validItems = storageParsedItems.filter((_item, index) => results[index]);
                localStorage.setItem('storageCartItems', JSON.stringify(validItems));
            } catch (error) {
                console.error('Ошбика чтения элементов из localStorage:', error);
            }
        };

        fetchItems();
    }, []);


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
    )
}
