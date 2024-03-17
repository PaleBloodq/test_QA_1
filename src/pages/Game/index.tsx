import { useParams } from "react-router"
import { useGetProductQuery } from "../../services/productsApi"
import { gameType } from "../../types/gameType"
import Container from "../../components/common/Container"
import Tag from "../../components/common/Tag"
import SelectPublication from "../../components/common/SelectPublictaion"
import { useEffect, useState } from "react"
import { useDispatch, useSelector } from "react-redux"
import { setSelectedPublication } from "../../features/Game/publicationSlice"
// import { getDiscount } from "../../hooks/getDiscount"
import { selectedPublicationSelector } from "../../features/Game/publicationSelectors"

export default function Game() {

    const dispatch = useDispatch()

    type GamePageType = {
        data?: gameType,
        isLoading: boolean,
    }

    const { gameId } = useParams()

    const { data, isLoading }: GamePageType = useGetProductQuery(gameId)
    const selectedPublication = useSelector(selectedPublicationSelector)

    useEffect(() => {
        if (data?.publications) {
            dispatch(setSelectedPublication(data.publications[0].id))
        }
    }, [data])



    return (
        <Container>
            <div className="flex flex-col items-center">
                {!isLoading && data !== undefined ? (
                    <div className="flex flex-col items-start">
                        <img className="w-[346px] h-[400px] rounded-xl mb-8 object-cover" src={data.photoUrls[0]} alt="game image" />
                        <h1 className="text-header mb-6">{data.title}</h1>
                        <div className="flex items-center">
                            <h1 className="price-big">275 ₽</h1>
                            <div className="flex">
                                {data.discount?.percent !== 0 && (
                                    <Tag type="discount">-{data.discount?.percent}%</Tag>
                                )}
                                {data.cashback !== 0 && <Tag type="cashback">Кэшбэк: {data.cashback}</Tag>}
                            </div>
                        </div>
                        {
                            data.discount && (
                                <div className="w-full flex justify-between mb-5">
                                    <p className="text-subtitle">Скидка действует до:</p>
                                    <p className="text-subtitle-info">{data.discount.deadline}</p>
                                </div>
                            )
                        }
                        <SelectPublication publications={data.publications} selectedPublication={selectedPublication} setSelectedPublication={setSelectedPublication} />
                    </div>
                ) : (<h1>Страница не найдена</h1>)
                }
            </div>
        </Container>
    )
}
