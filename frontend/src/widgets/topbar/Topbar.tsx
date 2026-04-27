import { uiText } from '../../shared/constants/ui-text'

export function Topbar() {
    return (
        <header className="topbar">
            <div>
                <h1 className="topbar__title">{uiText.app.title}</h1>
                <p className="topbar__subtitle">{uiText.app.subtitle}</p>
            </div>
        </header>
    )
}