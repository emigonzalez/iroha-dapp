const Card = ({title, description}) => {
    return (
        <div className="card bg-dark text-white">
            <div className="card-body">
                <h5 className="card-title">{title}</h5>
                <span className="card-text fs-6">{description}</span>
            </div>
        </div>
    )
}

export default Card;
