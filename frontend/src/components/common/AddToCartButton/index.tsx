import { useDispatch, useSelector } from "react-redux";
import { addToCart } from "../../../features/Cart/cartSlice";
import Button from "../Button";
import { cartSelector } from "../../../features/Cart/cartSelectors";
import { CartItemType } from "../../../types/cartItem";

export default function AddToCartButton({ cartItem }: { cartItem: CartItemType }) {
    const dispatch = useDispatch();

    const { items } = useSelector(cartSelector)
    const isAdded = items?.find((item) => item?.id === cartItem?.id) || false

    return (
        <>
            <div className="w-full h-[80px] bg-[#161616] fixed bottom-0 left-0 flex justify-center items-start">
                <div className='w-[345px] mt-[-5px]'>
                    <Button onClick={() => dispatch(addToCart(cartItem))}>{!isAdded ? 'Добавить в корзину' : 'В корзине'}</Button>
                </div>
            </div>
            <div className='h-16'></div>
        </>
    )
}
