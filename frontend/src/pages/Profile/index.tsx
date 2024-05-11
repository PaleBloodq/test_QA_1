import React, { useEffect, useState } from "react";
import Container from "../../components/common/Container";
import Tag from "../../components/common/Tag";
import { useGetOrdersQuery, useUpdateUserDataMutation } from "../../services/userApi";
import Input from "../../components/common/Input";
import Button from "../../components/common/Button";
import { OrderType } from "../../types/orderType";
import { useDispatch, useSelector } from "react-redux";
import { setUserName, updateAccountMail, updateAccountPassword, updateBillMail } from "../../features/User/userSlice";
import { userSelector } from "../../features/User/userSelectors";
import Navigation from "../../components/common/Navigation";
import { useNavigate } from "react-router";

export default function Profile() {
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const { data: ordersData = [], isLoading: isOrdersLoading, error: ordersError } = useGetOrdersQuery({})
    const [showOrderHistory, setShowOrderHistory] = useState(false)
    const { userData, updatedData, username, isLoggined } = useSelector(userSelector)
    const [updateUserData] = useUpdateUserDataMutation();

    function handleUpdateUserData() {
        updateUserData({ updatedData })
    }


    useEffect(() => {
        dispatch(setUserName(`${window.Telegram?.WebApp.initDataUnsafe.user.first_name || ''} ${window.Telegram?.WebApp.initDataUnsafe.user.last_name || ''}`))
    }, [])
    // useEffect(() => {
    //     dispatch(setUserName(`123`))
    // }, [])





    function orderStatusIcon(status: "PAID" | "ERROR" | "OK" | "PAYMENT" | "IN_PROGRESS" | "COMPLETED"): React.ReactNode {
        switch (status) {
            case 'PAID':
                return (<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8 0C12.4183 0 16 3.58172 16 8C16 12.4183 12.4183 16 8 16C3.58172 16 0 12.4183 0 8C0 3.58172 3.58172 0 8 0ZM10.4636 5.6636L6.9 9.22721L5.5364 7.8636C5.18492 7.51213 4.61508 7.51213 4.2636 7.8636C3.91213 8.21508 3.91213 8.78492 4.2636 9.1364L6.2636 11.1364C6.61508 11.4879 7.18492 11.4879 7.5364 11.1364L11.7364 6.9364C12.0879 6.58492 12.0879 6.01508 11.7364 5.6636C11.3849 5.31213 10.8151 5.31213 10.4636 5.6636Z" fill="#46A027" />
                </svg>)
            case 'COMPLETED':
                return (<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8 0C12.4183 0 16 3.58172 16 8C16 12.4183 12.4183 16 8 16C3.58172 16 0 12.4183 0 8C0 3.58172 3.58172 0 8 0ZM10.4636 5.6636L6.9 9.22721L5.5364 7.8636C5.18492 7.51213 4.61508 7.51213 4.2636 7.8636C3.91213 8.21508 3.91213 8.78492 4.2636 9.1364L6.2636 11.1364C6.61508 11.4879 7.18492 11.4879 7.5364 11.1364L11.7364 6.9364C12.0879 6.58492 12.0879 6.01508 11.7364 5.6636C11.3849 5.31213 10.8151 5.31213 10.4636 5.6636Z" fill="#46A027" />
                </svg>)
            case "OK":
                return (<svg fill="#ababab" width="20px" height="20px" viewBox="0 0 24.00 24.00" xmlns="http://www.w3.org/2000/svg" stroke="#ababab" strokeWidth="0.00024000000000000003"><g id="SVGRepo_bgCarrier" strokeWidth="0"><rect x="0" y="0" width="24.00" height="24.00" rx="12" fill="#ffffff" strokeWidth="0"></rect></g><g id="SVGRepo_tracerCarrier" strokeLinecap="round" strokeLinejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M12 21a9 9 0 1 1 9-9 9.01 9.01 0 0 1-9 9zm0-16a7 7 0 1 0 7 7 7.008 7.008 0 0 0-7-7z"></path> <path d="M15.03 14.75a1 1 0 0 1-.5-.134l-3.03-1.75A1 1 0 0 1 11 12V7.5a1 1 0 0 1 2 0v3.923l2.531 1.461a1 1 0 0 1-.501 1.866z"></path> </g></svg>)
            case "PAYMENT":
                return (<svg fill="#ababab" width="20px" height="20px" viewBox="0 0 24.00 24.00" xmlns="http://www.w3.org/2000/svg" stroke="#ababab" strokeWidth="0.00024000000000000003"><g id="SVGRepo_bgCarrier" strokeWidth="0"><rect x="0" y="0" width="24.00" height="24.00" rx="12" fill="#ffffff" strokeWidth="0"></rect></g><g id="SVGRepo_tracerCarrier" strokeLinecap="round" strokeLinejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M12 21a9 9 0 1 1 9-9 9.01 9.01 0 0 1-9 9zm0-16a7 7 0 1 0 7 7 7.008 7.008 0 0 0-7-7z"></path> <path d="M15.03 14.75a1 1 0 0 1-.5-.134l-3.03-1.75A1 1 0 0 1 11 12V7.5a1 1 0 0 1 2 0v3.923l2.531 1.461a1 1 0 0 1-.501 1.866z"></path> </g></svg>)
            case "IN_PROGRESS":
                return (<svg fill="#ababab" width="20px" height="20px" viewBox="0 0 24.00 24.00" xmlns="http://www.w3.org/2000/svg" stroke="#ababab" strokeWidth="0.00024000000000000003"><g id="SVGRepo_bgCarrier" strokeWidth="0"><rect x="0" y="0" width="24.00" height="24.00" rx="12" fill="#ffffff" strokeWidth="0"></rect></g><g id="SVGRepo_tracerCarrier" strokeLinecap="round" strokeLinejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M12 21a9 9 0 1 1 9-9 9.01 9.01 0 0 1-9 9zm0-16a7 7 0 1 0 7 7 7.008 7.008 0 0 0-7-7z"></path> <path d="M15.03 14.75a1 1 0 0 1-.5-.134l-3.03-1.75A1 1 0 0 1 11 12V7.5a1 1 0 0 1 2 0v3.923l2.531 1.461a1 1 0 0 1-.501 1.866z"></path> </g></svg>)
            case "ERROR":
                return (<svg fill="#ffffff" width="16px" height="16px" viewBox="-0.96 -0.96 25.92 25.92" xmlns="http://www.w3.org/2000/svg" stroke="#ffffff" strokeWidth="0.00024000000000000003"><g id="SVGRepo_bgCarrier" strokeWidth="0" transform="translate(0,0), scale(1)"><rect x="-0.96" y="-0.96" width="25.92" height="25.92" rx="12.96" fill="#d11515" strokeWidth="0"></rect></g><g id="SVGRepo_tracerCarrier" strokeLinecap="round" strokeLinejoin="round" stroke="#CCCCCC" strokeWidth="0.288"></g><g id="SVGRepo_iconCarrier"> <path d="M13.414 12l4.95-4.95a1 1 0 0 0-1.414-1.414L12 10.586l-4.95-4.95A1 1 0 0 0 5.636 7.05l4.95 4.95-4.95 4.95a1 1 0 0 0 1.414 1.414l4.95-4.95 4.95 4.95a1 1 0 0 0 1.414-1.414z"></path> </g></svg>)
        }
    }

    return (
        <Container>
            {isLoggined ? <>
                <div className="w-full h-[100px] custom-border px-6 flex items-center justify-start">
                    {!isOrdersLoading &&
                        <>
                            <div className="w-14 h-14 rounded-full bg-blue-400 mr-6"></div>
                            <div className="flex flex-col gap-[10px]">
                                <h1 className="text-title-xl">{username}</h1>
                                <div className="flex gap-4">
                                    <p className="text-subtitle">Баллы:</p>
                                    <Tag type="discount">{userData?.cashback} ₽</Tag>
                                </div>
                            </div>
                        </>
                    }
                </div>
                <div className="w-full flex gap-3 mt-6">
                    <button onClick={() => setShowOrderHistory(false)} className={`w-full h-[33px] text-[14px] ${!showOrderHistory ? "rounded-lg red-gradient font-bold text-white" : "rounded-lg border dark:border-[#FFFFFF1A] text-[#606D7B] dark:text-[#FFFFFF99]"} `} >
                        Данные покупателя
                    </button>
                    <button onClick={() => setShowOrderHistory(true)} className={`w-full h-[33px] text-[14px] ${showOrderHistory ? "rounded-lg red-gradient font-bold text-white" : "rounded-lg border dark:border-[#FFFFFF1A] text-[#606D7B] dark:text-[#FFFFFF99]"} `} >
                        История заказов
                    </button>
                </div>
                {!showOrderHistory
                    ?
                    <div className="w-full flex flex-col mt-7">
                        <p className="text-subtitle mb-3">E-mail от аккаунта PlayStation:</p>
                        <Input localValue={false} hardlyEditable={true} placeholder="E-Mail" type="email" value={updatedData.psEmail} setValue={updateAccountMail} />
                        <p className="text-subtitle mb-3">Пароль от аккаунта PlayStation:</p>
                        <Input localValue={false} hardlyEditable={true} placeholder="Пароль" type="password" value={updatedData.psPassword} setValue={updateAccountPassword} />
                        <p className="text-subtitle mb-3">E-mail для чеков:</p>
                        <Input localValue={false} hardlyEditable={true} placeholder="E-Mail" type="email" value={updatedData.billEmail} setValue={updateBillMail} />
                        <span className="mt-36">
                            <Button onClick={handleUpdateUserData}>Сохранить изменения</Button>
                        </span>
                    </div>
                    :
                    <div className="w-full flex flex-col mt-7 gap-[13px]">
                        {ordersData.length > 0 ? ordersData?.map((order: OrderType, index: number) =>
                            <div key={index} className="w-full custom-border p-5 flex flex-col">
                                <div className="flex w-full justify-between mb-6">
                                    <h1 className="text-title">Заказ от {order.date}</h1>
                                    <div className="flex gap-2 items-center">
                                        <h2 className="text-title">{order.amount} ₽</h2>
                                        {orderStatusIcon(order.status)}
                                    </div>
                                </div>
                                <div className="w-full flex flex-col">
                                    {order.order_products.map((cartItem, index: number) => <React.Fragment key={index} >
                                        <div className="flex flex-col gap-1">
                                            <h1 className="text-title-sm">{cartItem.item}</h1>
                                            <p className="text-subtitle">{cartItem.description}</p>
                                            <h2 className="text-title">{cartItem.final_price} ₽</h2>
                                        </div>
                                        {index !== order.order_products.length - 1 && <div className="w-full h-[1px] bg-[#E7E7E8] dark:bg-[#FFFFFF0D] my-6"></div>}
                                    </React.Fragment>
                                    )}
                                </div>
                                {order.status === "PAYMENT" ? <Button onClick={() => window.location.href = (order.payment_url)}>Оплатить</Button> : <></>}
                            </div>
                        ) :
                            (<div className="h-96 flex justify-center">
                                <h1 className="text-title">Тут будут ваши заказаы</h1>
                            </div>)}
                    </div>
                }
            </> : <>
                <Navigation />
                <div className="flex flex-col gap-7 my-52">
                    <h1 className="text-header text-center">Профиль появится автоматически после вашего первого заказа</h1>
                    <Button onClick={() => navigate(-1)}>Вернуться к каталогу</Button>
                </div>
            </>
            }
        </Container >
    )
}
