import { useParams } from "react-router"
import { useGetProductQuery } from "../../services/productsApi"
import { gameType } from "../../types/gameType"
import Container from "../../components/common/Container"
import Tag from "../../components/common/Tag"

export default function Game() {

    type GamePageType = {
        data: gameType | undefined,
        isLoading: boolean,
    }

    const { gameId } = useParams()

    const { data, isLoading }: GamePageType = useGetProductQuery(gameId)

    console.log(data)

    return (
        <Container>
            <div className="flex flex-col items-center">
                {!isLoading && data !== undefined ? (
                    <div className="flex flex-col items-start">
                        <img className="w-[346px] h-[400px] rounded-xl mb-8 object-cover" src={data.img} alt="game image" />
                        <h1 className="text-header mb-6">{data.name}</h1>
                        <div className="flex items-center">
                            <h1 className="price-big">275 ₽</h1>
                            <div className="flex">
                                {data.discount?.percent !== undefined && (
                                    <Tag type="discount">-{data.discount?.percent}%</Tag>
                                )}
                                {data.cashback !== '' && <Tag type="cashback">Кэшбэк: {data.cashback}</Tag>}
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
                        <h2 className="text-title text-[18px]">Издания</h2>
                    </div>
                ) : (<h1>Страница не найдена</h1>)
                }
            </div>
        </Container>
    )
}
