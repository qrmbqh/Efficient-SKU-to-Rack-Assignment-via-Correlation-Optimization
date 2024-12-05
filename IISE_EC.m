function racks = IISE_EC(A, C_in, midu)
tic;
B_in = A * C_in;
F_in = sum(sum(B_in ~= 0));
B_best = B_in;
F_best = F_in;
restart = 1;
maxchainlength = int64(0.9 * size(B_in,2));
tabulength = int64(0.6 * maxchainlength);
while restart == 1
    for rack_j = 1:size(C_in,2)
        skus = find(C_in(:,rack_j)).';
        for sku_i = skus
            step = 1;
            tabulist = zeros(1,tabulength);
            sourcerack = rack_j;
            bestchange = 10000000;
            [~, targetrack, bestchange] = algorithm5(A,B_in,C_in,sourcerack,sku_i,bestchange);
            F_ref = F_in + bestchange;
            tabulist(step) = sku_i;
            step = step + 1;
            %if size(tabulist,2) >= tabulength
            %    tabulist = tabulist(size(tabulist,2)-tabulength+1:end);
            %end
            C_ref = C_in;
            C_ref(sku_i,sourcerack) = 0;
            C_ref(sku_i,targetrack) = 1;
            B_ref = A * C_ref;
            sourcerack = targetrack;
            [bestchange, sku_l] = algorithm6(A, B_ref, C_ref, sourcerack, rack_j, tabulist);
            if F_ref + bestchange < F_best
                F_best = F_ref + bestchange;
                C_best = C_ref;
                C_best(sku_l,sourcerack) = 0;
                C_best(sku_l,rack_j) = 1;
                B_best = A * C_best;
            end
            for chainlength = 2:maxchainlength
                skus2 = find(C_ref(:,sourcerack)).';
                nontabu_skus = ~ismember(skus2,tabulist);
                if sum(nontabu_skus) == 0
                    break;
                else
                    bestchange = 10000000;
                    sku = 0;
                    targetrack = 0;
                    for nontabu = 1:size(nontabu_skus,2)
                        if nontabu_skus(nontabu) == 1
                            bestchange_temp = 10000000;
                            nontabusku = skus2(nontabu);
                            [sku_temp, targetrack_temp, bestchange_temp] = algorithm5(A,B_ref,C_ref,sourcerack,nontabusku,bestchange_temp);
                            if bestchange_temp < bestchange
                                bestchange = bestchange_temp;
                                sku = sku_temp;
                                targetrack = targetrack_temp;
                            end
                        end
                    end
                    %disp([chainlength,sku,sourcerack,targetrack]);
                    %chainlength = chainlength+1;
                    F_ref = F_ref + bestchange;
                    tabulist(step) = sku;
                    step = step + 1;
                    if step > tabulength
                        step = 1;
                    end
                    %if size(tabulist,2) > tabulength
                    %    tabulist = tabulist(size(tabulist,2)-tabulength+1:end);
                    %end
                    C_ref(sku,sourcerack) = 0;
                    C_ref(sku,targetrack) = 1;
                    B_ref = A * C_ref;
                    sourcerack = targetrack;
                    if sum(C_ref(:,sourcerack)) == midu 
                        if F_ref < F_best
                            F_best = F_ref;
                            C_best = C_ref;
                            B_best = A * C_best;
                        end
                    else
                        sourcerack2 = find(sum(C_ref) == midu+1);
                        targetrack2 = find(sum(C_ref) == midu-1);
                        [bestchange, sku2] = algorithm6(A,B_ref,C_ref,sourcerack2,targetrack2,tabulist);
                        if F_ref + bestchange < F_best
                            F_best = F_ref + bestchange;
                            C_best = C_ref;
                            C_best(sku2,sourcerack2) = 0;
                            C_best(sku2,targetrack2) = 1;
                            B_best = A * C_best;
                        end
                    end
                end
            end
        end
    end
    if F_best < F_in
        F_in = F_best;
        B_in = B_best;
        C_in = C_best;
        restart = 1;
    else
        restart = 0;
    end
end
racks = cell(size(C_in,2),1);
for i = 1:size(C_in,2)
        members = find(C_in(:,i)).';
        racks{i} = members;
end


