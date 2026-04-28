import { useEffect, useState } from 'react'

import { getPreferences, updatePreferences } from '../../entities/user/api/preferences.api'
import { getCapabilities } from '../../entities/user/api/capabilities.api'
import { uiText } from '../../shared/constants/ui-text'

export function ProfilePage() {
    const [prefs, setPrefs] = useState<any>(null)
    const [caps, setCaps] = useState<any>(null)
    const [saving, setSaving] = useState(false)

    useEffect(() => {
        getPreferences().then(setPrefs)
        getCapabilities().then(setCaps)
    }, [])

    if (!prefs || !caps) {
        return <div className="page">{uiText.common.loading}</div>
    }

    const handleSave = async () => {
        setSaving(true)
        await updatePreferences(prefs)
        setSaving(false)
    }

    const modes = [
        {
            value: 'lexical',
            label: uiText.newRun.modes.lexical.label,
            description: uiText.newRun.modes.lexical.description,
        },
        {
            value: 'semantic',
            label: uiText.newRun.modes.semantic.label,
            description: uiText.newRun.modes.semantic.description,
        },
        {
            value: 'semantic_llm',
            label: uiText.newRun.modes.semanticLlm.label,
            description: uiText.newRun.modes.semanticLlm.description,
        },
    ]

    return (
        <div className="page">
            <div className="card profile-card">
                <h2 className="section-title">Настройки</h2>

                {/* Режим анализа */}
                <div className="field">
                    <label className="label">
                        {uiText.newRun.searchModeLabel}
                    </label>

                    <div className="mode-grid">
                        {modes.map((mode) => {
                            const active = prefs.default_search_mode === mode.value

                            return (
                                <div
                                    key={mode.value}
                                    className={`mode-card ${active ? 'mode-card--active' : ''}`}
                                    onClick={() =>
                                        setPrefs({
                                            ...prefs,
                                            default_search_mode: mode.value,
                                        })
                                    }
                                >
                                    <div className="mode-title">{mode.label}</div>
                                    <div className="mode-description">
                                        {mode.description}
                                    </div>
                                </div>
                            )
                        })}
                    </div>
                </div>

                {/* Провайдер */}
                <div className="field">
                    <label className="label">Провайдер модели</label>

                    <div className="provider-grid">
                        {caps.llm_providers.map((p: any) => {
                            const active = prefs.preferred_llm_provider === p.code

                            return (
                                <div
                                    key={p.code}
                                    className={`provider-card 
                    ${active ? 'provider-card--active' : ''} 
                    ${!p.enabled ? 'provider-card--disabled' : ''}`}
                                    onClick={() => {
                                        if (!p.enabled) return

                                        setPrefs({
                                            ...prefs,
                                            preferred_llm_provider: p.code,
                                        })
                                    }}
                                >
                                    <div className="provider-title">{p.label}</div>

                                    {!p.enabled && (
                                        <div className="provider-disabled">
                                            Недоступно
                                        </div>
                                    )}
                                </div>
                            )
                        })}
                    </div>
                </div>

                {/* Кнопка */}
                <div className="profile-actions">
                    <button
                        className="button"
                        disabled={saving}
                        onClick={handleSave}
                    >
                        {saving ? 'Сохранение...' : 'Сохранить'}
                    </button>
                </div>
            </div>
        </div>
    )
}