import { useDispatch, useSelector } from "react-redux";
import { addToCart } from "../../../features/Cart/cartSlice";
import Button from "../Button";
import { cartSelector } from "../../../features/Cart/cartSelectors";

export default function AddToCartButton({ cartItem }) {
    const dispatch = useDispatch();

    const { items } = useSelector(cartSelector)
    const isAdded = items?.find((item) => item?.id === cartItem?.id) || false

    return (
        <>
            <div className='w-[345px] fixed bottom-4'>
                <Button onClick={() => dispatch(addToCart(cartItem))}>{!isAdded ? 'Добавить в корзину' : 'В корзине'}</Button>
            </div>
            <div className='h-16'></div>
        </>
    )
}
