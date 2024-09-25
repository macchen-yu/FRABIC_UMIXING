import numpy as np


def NCLS(MatrixZ, x):
    # input MatrixZ: signatures of endmembers, size [bands, p]
    # input x: the signature whose abundance is to be estimated
    # output abundance: abundance of each material in x, size [p, 1]
    # output error_vector: error vector, size [bands, 1]

    M = MatrixZ.shape[1]
    R = np.zeros(M)
    P = np.ones(M)
    invMtM = np.linalg.inv(np.dot(MatrixZ.T, MatrixZ))
    Alpha_ls = np.dot(invMtM, np.dot(MatrixZ.T, x))

    Alpha_ncls = Alpha_ls.copy()
    min_Alpha_ncls = np.min(Alpha_ncls)
    tol = 1e-7

    while min_Alpha_ncls < -tol:
        for II in range(M):
            if Alpha_ncls[II] < 0 and P[II] == 1:
                R[II] = 1
                P[II] = 0

        goto_step6 = True
        counter = 0

        while goto_step6:
            index_for_Lamda = np.where(R == 1)[0]
            Alpha_R = Alpha_ls[index_for_Lamda]
            Sai = invMtM[np.ix_(index_for_Lamda, index_for_Lamda)]

            inv_Sai = np.linalg.inv(Sai)
            Lamda = np.dot(inv_Sai, Alpha_R)

            max_Lamda = np.max(Lamda)
            index_Max_Lamda = np.argmax(Lamda)
            counter += 1
            if max_Lamda <= 0 or counter == 200:
                break

            inv_Sai_ex = inv_Sai.copy()
            inv_Sai_ex[0, :] = inv_Sai[index_Max_Lamda, :]
            inv_Sai_ex[:, 0] = inv_Sai[:, index_Max_Lamda]

            inv_Sai_next = inv_Sai_ex[1:, 1:] - np.outer(inv_Sai_ex[1:, 0], inv_Sai_ex[0, 1:]) / inv_Sai_ex[0, 0]

            P[index_for_Lamda[index_Max_Lamda]] = 1
            R[index_for_Lamda[index_Max_Lamda]] = 0
            index_for_Lamda = np.delete(index_for_Lamda, index_Max_Lamda)

            Alpha_R = Alpha_ls[index_for_Lamda]
            Lamda = np.dot(inv_Sai_next, Alpha_R)

            Phai_column = invMtM[:, index_for_Lamda]

            if Phai_column.size != 0:
                Alpha_s = Alpha_ls - np.dot(Phai_column, Lamda)
            else:
                Alpha_s = Alpha_ls

            goto_step6 = False

            for II in range(M):
                if S[II] == 1 and Alpha_s[II] < 0:
                    P[II] = 0
                    R[II] = 1
                    goto_step6 = True

        index_for_Phai = np.where(R == 1)[0]
        Phai_column = invMtM[:, index_for_Phai]

        if Phai_column.size != 0:
            Alpha_ncls = Alpha_ls - np.dot(Phai_column, Lamda)
        else:
            Alpha_ncls = Alpha_ls

        min_Alpha_ncls = np.min(Alpha_ncls)

    abundance = np.zeros(M)
    for II in range(M):
        if Alpha_ncls[II] > 0:
            abundance[II] = Alpha_ncls[II]

    error_vector = np.dot(MatrixZ, abundance) - x
    return abundance, error_vector


# # 使用範例
# MatrixZ = np.random.rand(200, 3)  # 模擬 200 個波段和 3 種端元
# x = np.random.rand(200)  # 模擬觀測到的像素光譜特徵
#
# # 調用 NCLS 函數進行豐度估計
# abundance, error_vector = NCLS(MatrixZ, x)
#
# # 輸出結果
# print('豐度估計:')
# print(abundance)
#
# print('誤差向量:')
# print(error_vector)

