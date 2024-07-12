import { useNavigate } from "react-router";
import { animated, useSpring } from 'react-spring';
import { useEffect, useState } from "react";
import { useAddToCartMutation, useGetCartQuery } from "../../../services/cartApi";
import { CartItemType } from "../../../types/cartItem";
import Button from "../Button";

export default function AddToCartButton({ cartItem }: { cartItem: CartItemType }) {
    const navigate = useNavigate();
    const { data: items } = useGetCartQuery({});
    const [addToCart, { data: newCart }] = useAddToCartMutation();
    const [isAdded, setIsAdded] = useState(false);
    const [firstClick, setFirstClick] = useState(false);

    useEffect(() => {
        const checkItemInCart = (cartData: CartItemType[]): boolean => {
            if (cartData) {
                const allItems = [...cartData];
                return allItems?.find((item) => item?.id === cartItem?.id) ? true : false
            }
            return false;
        };

        setIsAdded(checkItemInCart(newCart) || checkItemInCart(items));
    }, [newCart, items, cartItem]);

    const addToCartHandler = (cartItem: CartItemType) => {
        if (!isAdded) {
            addToCart({ id: cartItem.id });
        } else {
            navigate('/cart');
        }
    };

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
            setFirstClick(false);
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
    );
}