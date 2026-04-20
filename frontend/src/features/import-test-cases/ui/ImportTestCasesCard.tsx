import {type ChangeEvent, useState } from 'react'

import { useImportTestCasesFileMutation } from '../../../entities/test-case/api/useImportTestCasesFileMutation'

type ImportTestCasesCardProps = {
    projectId: number
}

export function ImportTestCasesCard({ projectId }: ImportTestCasesCardProps) {
    const importMutation = useImportTestCasesFileMutation({ projectId })
    const [selectedFile, setSelectedFile] = useState<File | null>(null)

    const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0] ?? null
        setSelectedFile(file)
    }

    const handleImport = async () => {
        if (!selectedFile) {
            return
        }

        await importMutation.mutateAsync(selectedFile)
        setSelectedFile(null)
    }

    return (
        <div className="card">
            <h3 className="section-title">Импорт test cases</h3>

            <div className="upload-panel">
                <div className="field">
                    <label className="label" htmlFor="test-cases-file">
                        JSON-файл
                    </label>

                    <input
                        id="test-cases-file"
                        className="input"
                        type="file"
                        accept=".json,application/json"
                        onChange={handleFileChange}
                    />
                </div>

                <div className="upload-panel__meta">
                    <p className="muted-text">
                        Поддерживается JSON-файл формата с корневым полем <code>items</code>.
                    </p>

                    {selectedFile ? (
                        <p className="upload-panel__filename">
                            Выбран файл: <strong>{selectedFile.name}</strong>
                        </p>
                    ) : null}
                </div>

                {importMutation.isError ? (
                    <p className="error-text">
                        Не удалось импортировать файл. Проверь формат JSON и доступность backend.
                    </p>
                ) : null}

                {importMutation.isSuccess ? (
                    <p className="success-text">Файл успешно импортирован.</p>
                ) : null}

                <div className="form-actions">
                    <button
                        className="button"
                        type="button"
                        disabled={!selectedFile || importMutation.isPending}
                        onClick={handleImport}
                    >
                        {importMutation.isPending ? 'Импорт...' : 'Импортировать файл'}
                    </button>
                </div>
            </div>
        </div>
    )
}