import { useParams } from "react-router"
import { useGetProductQuery } from "../../services/productsApi"
import { gameType } from "../../types/gameType"
import Container from "../../components/common/Container"
import Tag from "../../components/common/Tag"
import SelectPublication from "../../components/common/SelectPublictaion"
import { useEffect } from "react"
import { useDispatch, useSelector } from "react-redux"
import { setSelectedPublication } from "../../features/Game/publicationSlice"
import { currentPriceSelector } from "../../features/Game/currentPriceSelectors"
import { setCurrentPrice } from "../../features/Game/currentPriceSlice"
import { getDiscount } from "../../hooks/getDiscount"
import { selectedPlatformSelector, selectedPublicationSelector } from "../../features/Game/publicationSelectors"
// import { getDiscount } from "../../hooks/getDiscount"

export default function Game() {

    const dispatch = useDispatch()

    type GamePageType = {
        data?: gameType,
        isLoading: boolean,
    }

    const { gameId } = useParams()

    const { data, isLoading }: GamePageType = useGetProductQuery(gameId)
    const selectedPublication = useSelector(selectedPublicationSelector)
    const selectedPlatform = useSelector(selectedPlatformSelector)

    useEffect(() => {
        if (data?.publications) {
            dispatch(setSelectedPublication(data.publications[0].id))
        }
    }, [data])

    const currentPrice = useSelector(currentPriceSelector)

    useEffect(() => {
        dispatch(setCurrentPrice(data?.publications
            .find((publication) => publication.id === selectedPublication).price
            .find((price) => price.platform === selectedPlatform).price))
    }, [selectedPublication, selectedPlatform])




    return (
        <Container>
            <div className="flex flex-col items-center">
                {!isLoading && data !== undefined ? (
                    <div className="flex flex-col items-start">
                        <img className="w-[346px] h-[400px] rounded-xl mb-8 object-cover" src={data.photoUrls[0]} alt="game image" />
                        <h1 className="text-header mb-6">{data.title}</h1>
                        <div className="flex items-center">
                            <h1 className="price-big">
                                {
                                    data.publications.find((publ) => publ.id === selectedPublication)?.psPlusDiscount ?
                                        getDiscount(currentPrice, data.publications.find((publ) => publ.id === selectedPublication)?.psPlusDiscount)
                                        : getDiscount(currentPrice, data.publications.find((publ) => publ.id === selectedPublication)?.discount.percent)
                                } ₽
                            </h1>
                            <div className="flex">
                                {data.discount?.percent !== 0 && (
                                    <Tag type="discount">-{data.publications.find((publ) => publ.id === selectedPublication)?.discount.percent}%</Tag>
                                )}
                                {/* {data.cashback !== 0 && <Tag type="cashback">Кэшбэк: {data.cashback}</Tag>} */}
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
                        <SelectPublication publications={data.publications} />
                    </div>
                ) : (<h1>Страница не найдена</h1>)
                }
            </div>
        </Container>
    )
}
