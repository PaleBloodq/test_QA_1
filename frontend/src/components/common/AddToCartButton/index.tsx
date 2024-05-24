import { useDispatch, useSelector } from "react-redux";
import { addToCart } from "../../../features/Cart/cartSlice";
import Button from "../Button";
import { cartSelector } from "../../../features/Cart/cartSelectors";
import { CartItemType } from "../../../types/cartItem";
import { useNavigate } from "react-router";
import { animated, useSpring } from 'react-spring'
import { useEffect, useState } from "react";

export default function AddToCartButton({ cartItem }: { cartItem: CartItemType }) {
    const dispatch = useDispatch();
    const navigate = useNavigate()
    const { items } = useSelector(cartSelector)
    const isAdded = items?.find((item) => item?.id === cartItem?.id) || false
    const [firstClick, setFirstClick] = useState(false);



    function addToCartHandler(cartItem: CartItemType) {
        if (!isAdded) {
            dispatch(addToCart(cartItem))
        } else {
            navigate('/cart')
        }
    }

    const props = useSpring({
        from: firstClick ? { left: "0", opacity: 0 } : null,
        to: firstClick ? [
            { left: "172.5px", opacity: 1 },
            { left: "345px", opacity: 0 }
        ] : null,
        loop: false,
        config: {
            duration: 250
        },
        onRest: () => {
            setFirstClick(false)
        }
    });

    useEffect(() => {
        if (isAdded) {
            setFirstClick(true);
        }
    }, [isAdded]);

    return (
        <>

            <div className="w-full h-[80px] bg-[#161616] fixed bottom-0 left-0 flex justify-center items-start">
                <div className='w-[345px] mt-[-5px] relative'>
                    <animated.div style={props} className='w-2 h-[50px] bg-white absolute z-50 top-5 -skew-x-12 opacity-0' />
                    <Button onClick={() => addToCartHandler(cartItem)}>{!isAdded ? 'Добавить в корзину' : 'В корзине'}</Button>
                </div>
            </div>
            <div className='h-16'></div>
        </>
    )
}
