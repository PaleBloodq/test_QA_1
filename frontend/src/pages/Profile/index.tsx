import React, { useEffect, useState } from "react";
import Container from "../../components/common/Container";
import Tag from "../../components/common/Tag";
import { useGetOrdersQuery, useGetUserQuery, useUpdateUserDataMutation } from "../../services/userApi";
import Input from "../../components/common/Input";
import Button from "../../components/common/Button";
import { OrderType } from "../../types/orderType";
import { useDispatch } from "react-redux";
import { setUserData } from "../../features/User/userSlice";

export default function Profile() {
    const dispatch = useDispatch()

    const { data: userData = [], isLoading: isUserLoading, status } = useGetUserQuery({})
    const { data: ordersData = [], isLoading: isOrdersLoading } = useGetOrdersQuery({})
    const [showOrderHistory, setShowOrderHistory] = useState(false)
    const [accountPassword, setAccountPassword] = useState(userData?.playstation_password)
    const [accountMail, setAccountMail] = useState(userData?.playstation_email)
    const [billMail, setBillMail] = useState(userData?.bill_email)

    const [updateUserData, { data, isLoading, error }] = useUpdateUserDataMutation();


    useEffect(() => {
        setAccountMail(userData?.playstation_email)
        setBillMail(userData?.bill_email)
        setAccountPassword(userData?.playstation_password)
        dispatch(setUserData(userData))
    }, [userData])

    const updatedData = {
        psEmail: accountMail,
        psPassword: accountPassword,
        billEmail: billMail
    }

    function handleUpdateUserData() {
        updateUserData({ updatedData })
    }

    return (
        <Container>
            <div className="w-full h-[100px] custom-border px-6 flex items-center justify-start">
                {!isUserLoading &&
                    <>
                        <div className="w-14 h-14 rounded-full bg-blue-400 mr-6"></div>
                        <div className="flex flex-col gap-[10px]">
                            <h1 className="text-title-xl">{userData?.bill_email}</h1>
                            <div className="flex gap-4">
                                <p className="text-subtitle">Баллы:</p>
                                <Tag type="discount">{userData?.cashback} ₽</Tag>
                            </div>
                        </div>
                    </>
                }
            </div>
            <div className="w-full flex gap-3 mt-6">
                <button onClick={() => setShowOrderHistory(false)} className={`w-full h-[33px] text-[14px] ${!showOrderHistory ? "rounded-lg red-gradient font-bold text-white" : "rounded-lg border dark:border-[#FFFFFF1A] text-[#606D7B] dark:text-[#FFFFFF99]"}`} >
                    Данные покупателя
                </button>
                <button onClick={() => setShowOrderHistory(true)} className={`w-full h-[33px] text-[14px] ${showOrderHistory ? "rounded-lg red-gradient font-bold text-white" : "rounded-lg border dark:border-[#FFFFFF1A] text-[#606D7B] dark:text-[#FFFFFF99]"}`} >
                    История заказов
                </button>
            </div>
            {!showOrderHistory
                ?
                <div className="w-full flex flex-col mt-7">
                    <p className="text-subtitle mb-3">E-mail от аккаунта PlayStation:</p>
                    <Input localValue={true} hardlyEditable={true} placeholder="E-Mail" type="email" value={accountMail} setValue={setAccountMail} />
                    <p className="text-subtitle mb-3">Пароль от аккаунта PlayStation:</p>
                    <Input localValue={true} hardlyEditable={true} placeholder="Пароль" type="password" value={accountPassword} setValue={setAccountPassword} />
                    <p className="text-subtitle mb-3">E-mail для чеков:</p>
                    <Input localValue={true} hardlyEditable={true} placeholder="E-Mail" type="email" value={billMail} setValue={setBillMail} />
                    <span className="mt-36">
                        <Button onClick={handleUpdateUserData}>Сохранить изменения</Button>
                    </span>
                </div>
                :
                <div className="w-full flex flex-col mt-7 gap-[13px]">
                    {!isOrdersLoading && ordersData?.map((order: OrderType, index: number) =>
                        <div key={index} className="w-full custom-border p-5 flex flex-col">
                            <div className="flex w-full justify-between mb-6">
                                <h1 className="text-title">Заказ от {order.date}</h1>
                                <div className="flex gap-2 items-center">
                                    <h2 className="text-title">{order.amount} ₽</h2>
                                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M8 0C12.4183 0 16 3.58172 16 8C16 12.4183 12.4183 16 8 16C3.58172 16 0 12.4183 0 8C0 3.58172 3.58172 0 8 0ZM10.4636 5.6636L6.9 9.22721L5.5364 7.8636C5.18492 7.51213 4.61508 7.51213 4.2636 7.8636C3.91213 8.21508 3.91213 8.78492 4.2636 9.1364L6.2636 11.1364C6.61508 11.4879 7.18492 11.4879 7.5364 11.1364L11.7364 6.9364C12.0879 6.58492 12.0879 6.01508 11.7364 5.6636C11.3849 5.31213 10.8151 5.31213 10.4636 5.6636Z" fill="#46A027" />
                                    </svg>
                                </div>
                            </div>
                            <div className="w-full flex flex-col">
                                {order.order_products.map((cartItem, index: number) => <React.Fragment key={index} >
                                    <div className="flex flex-col gap-1">
                                        <h1 className="text-title-sm">{cartItem.item}</h1>
                                        <p className="text-subtitle">{cartItem.description}</p>
                                        <h2 className="text-title">{cartItem.price} ₽</h2>
                                    </div>
                                    {index !== order.order_products.length - 1 && <div className="w-full h-[1px] bg-[#E7E7E8] dark:bg-[#FFFFFF0D] my-6"></div>}
                                </React.Fragment>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            }
        </Container>
    )
}
