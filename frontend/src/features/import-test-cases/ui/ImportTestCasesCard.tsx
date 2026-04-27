import {type ChangeEvent, useState } from 'react'

import { useImportTestCasesFileMutation } from '../../../entities/test-case/api/useImportTestCasesFileMutation'
import { uiText } from '../../../shared/constants/ui-text'
import { getUserErrorMessage } from '../../../shared/lib/get-user-error-message'
import { useToast } from '../../../shared/ui/toast/useToast'

type ImportTestCasesCardProps = {
    projectId: number
}

export function ImportTestCasesCard({ projectId }: ImportTestCasesCardProps) {
    const importMutation = useImportTestCasesFileMutation({ projectId })
    const toast = useToast()
    const [selectedFile, setSelectedFile] = useState<File | null>(null)

    const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0] ?? null
        setSelectedFile(file)
    }

    const handleImport = async () => {
        if (!selectedFile) {
            return
        }

        try {
            const result = await importMutation.mutateAsync(selectedFile)

            if (result.status === 'completed') {
                toast.success('Файл загружен, тест-кейсы автоматически переиндексированы.')
            } else {
                toast.info(
                    'Файл загружен, но автоматическая переиндексация не завершилась. Ее можно запустить вручную.',
                )
            }

            setSelectedFile(null)
        } catch (error) {
            toast.error(getUserErrorMessage(error))
        }
    }

    return (
        <div className="card">
            <h3 className="section-title">{uiText.testCases.importTitle}</h3>

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
                        Поддерживается JSON-файл с корневым полем <code>items</code>. После загрузки
                        автоматически запускается переиндексация.
                    </p>

                    {selectedFile ? (
                        <p className="upload-panel__filename">
                            {uiText.testCases.selectedFilePrefix}{' '}
                            <strong>{selectedFile.name}</strong>
                        </p>
                    ) : null}
                </div>

                <div className="form-actions">
                    <button
                        className="button"
                        type="button"
                        disabled={!selectedFile || importMutation.isPending}
                        onClick={handleImport}
                    >
                        {importMutation.isPending
                            ? uiText.testCases.importingButton
                            : uiText.testCases.importButton}
                    </button>
                </div>
            </div>
        </div>
    )
}